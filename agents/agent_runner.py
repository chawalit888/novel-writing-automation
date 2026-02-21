#!/usr/bin/env python3
"""
Novel Empire Agent Runner
รัน agents และจัดการ lifecycle ของ agents
"""

import os
import sys
import json
import yaml
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.orchestrator import AgentOrchestrator, Message, MessageType, Priority


# ==========================================
# Logging Setup
# ==========================================
def setup_logging(agent_id: str, logs_dir: Path):
    """Setup logging for an agent"""
    log_file = logs_dir / f"{agent_id}.log"

    logger = logging.getLogger(agent_id)
    logger.setLevel(logging.INFO)

    # File handler
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# ==========================================
# Base Agent Class
# ==========================================
class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(self, config_path: str, orchestrator: AgentOrchestrator):
        self.config_path = Path(config_path)
        self.orchestrator = orchestrator

        # Load configuration
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        self.agent_id = self.config['agent']['id']
        self.agent_name = self.config['agent']['name']
        self.role = self.config['agent']['role']
        self.model = self.config['agent'].get('model', 'claude-sonnet-4')

        # Setup logging
        logs_dir = self.config_path.parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        self.logger = setup_logging(self.agent_id, logs_dir)

        self.running = False

    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """Process a single message. Override in subclasses."""
        pass

    def start(self):
        """Start the agent"""
        self.running = True
        self.logger.info(f"Agent {self.agent_name} started")

        while self.running:
            try:
                # Get pending messages
                messages = self.orchestrator.get_messages(self.agent_id)

                for message in messages:
                    self.logger.info(
                        f"Processing message: {message.subject}"
                    )

                    # Process the message
                    response = self.process_message(message)

                    # Acknowledge processed
                    self.orchestrator.acknowledge_message(
                        message.id, self.agent_id
                    )

                    # Send response if any
                    if response:
                        self.orchestrator.send_message(response)

                # Sleep before next check
                time.sleep(5)

            except KeyboardInterrupt:
                self.logger.info("Received shutdown signal")
                self.stop()
            except Exception as e:
                self.logger.error(f"Error in agent loop: {e}")
                time.sleep(10)  # Wait before retry

    def stop(self):
        """Stop the agent"""
        self.running = False
        self.logger.info(f"Agent {self.agent_name} stopped")

    def send_message(
        self,
        to_agent: str,
        message_type: MessageType,
        subject: str,
        body: Dict[str, Any],
        priority: Priority = Priority.NORMAL
    ) -> bool:
        """Send a message to another agent"""
        message = self.orchestrator.create_message(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            subject=subject,
            body=body,
            priority=priority
        )
        return self.orchestrator.send_message(message)

    def report_status(self, status: str, details: Dict = None):
        """Report status to manager"""
        reports_to = self.config.get('reports_to')
        if not reports_to:
            return

        body = {
            "agent_id": self.agent_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        if details:
            body["details"] = details

        self.send_message(
            to_agent=reports_to,
            message_type=MessageType.STATUS,
            subject=f"Status Update: {status}",
            body=body
        )


# ==========================================
# CEO Agent
# ==========================================
class CEOAgent(BaseAgent):
    """CEO Agent - Strategic oversight"""

    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages as CEO"""
        self.logger.info(f"CEO processing: {message.message_type}")

        if message.message_type == MessageType.TASK.value:
            # New task from user - distribute to teams
            return self._handle_new_task(message)

        elif message.message_type == MessageType.STATUS.value:
            # Status update from manager
            return self._handle_status_update(message)

        elif message.message_type == MessageType.ALERT.value:
            # Alert - may need escalation
            return self._handle_alert(message)

        elif message.message_type == MessageType.REPORT.value:
            # Report from manager
            return self._handle_report(message)

        return None

    def _handle_new_task(self, message: Message) -> Optional[Message]:
        """Handle new task assignment"""
        task = message.body

        # Determine which team
        team = self._determine_team(task)
        manager_id = {
            "claude-code": "mgr-claude-001",
            "n8n": "mgr-n8n-001"
        }.get(team, "mgr-n8n-001")

        self.logger.info(f"Assigning task to {team} team")

        # Create task for manager
        return self.orchestrator.create_message(
            from_agent=self.agent_id,
            to_agent=manager_id,
            message_type=MessageType.TASK,
            subject=f"Task Assignment: {task.get('title', 'New Task')}",
            body=task,
            priority=Priority(task.get('priority', 'normal')),
            requires_response=True
        )

    def _determine_team(self, task: Dict) -> str:
        """Determine best team for task"""
        quality = task.get('quality', 'standard')
        count = task.get('novel_count', 1)

        if quality in ['premium', 'high'] or count <= 3:
            return "claude-code"
        return "n8n"

    def _handle_status_update(self, message: Message) -> Optional[Message]:
        """Handle status updates"""
        self.logger.info(f"Status from {message.from_agent}: {message.body}")
        return None

    def _handle_alert(self, message: Message) -> Optional[Message]:
        """Handle alerts"""
        self.logger.warning(f"ALERT from {message.from_agent}: {message.body}")
        # Could escalate to human here
        return None

    def _handle_report(self, message: Message) -> Optional[Message]:
        """Handle reports"""
        self.logger.info(f"Report from {message.from_agent}")
        # Process and store report
        return None


# ==========================================
# Manager Agent (Base for both managers)
# ==========================================
class ManagerAgent(BaseAgent):
    """Manager Agent - Team coordination"""

    def __init__(self, config_path: str, orchestrator: AgentOrchestrator):
        super().__init__(config_path, orchestrator)
        self.team_members = self.config.get('team', {}).get('subagents', [])

    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages as Manager"""
        self.logger.info(f"Manager processing: {message.message_type}")

        if message.message_type == MessageType.TASK.value:
            return self._handle_task(message)

        elif message.message_type == MessageType.STATUS.value:
            return self._handle_subagent_status(message)

        elif message.message_type == MessageType.QUESTION.value:
            return self._handle_question(message)

        return None

    def _handle_task(self, message: Message) -> Optional[Message]:
        """Handle task from CEO"""
        task = message.body
        self.logger.info(f"Received task: {task.get('title')}")

        # Acknowledge receipt
        self._send_acknowledgement(message)

        # Distribute to subagents based on task type
        self._distribute_task(task)

        return None

    def _send_acknowledgement(self, message: Message):
        """Send acknowledgement to CEO"""
        self.send_message(
            to_agent="ceo-001",
            message_type=MessageType.STATUS,
            subject=f"Task Acknowledged: {message.subject}",
            body={
                "status": "acknowledged",
                "message_id": message.id,
                "action": "processing"
            }
        )

    def _distribute_task(self, task: Dict):
        """Distribute task to subagents - override in subclasses"""
        self.logger.info("Distributing task to subagents...")

    def _handle_subagent_status(self, message: Message) -> Optional[Message]:
        """Handle status from subagent"""
        self.logger.info(
            f"Subagent status: {message.from_agent} - {message.body}"
        )
        return None

    def _handle_question(self, message: Message) -> Optional[Message]:
        """Handle question from subagent"""
        self.logger.info(f"Question from {message.from_agent}")
        # Could escalate to CEO if needed
        return None


# ==========================================
# Subagent (Base for workers)
# ==========================================
class SubAgent(BaseAgent):
    """Subagent - Task execution"""

    def process_message(self, message: Message) -> Optional[Message]:
        """Process messages as Subagent"""
        self.logger.info(f"Subagent processing: {message.message_type}")

        if message.message_type == MessageType.TASK.value:
            return self._execute_task(message)

        return None

    def _execute_task(self, message: Message) -> Optional[Message]:
        """Execute assigned task"""
        task = message.body
        self.logger.info(f"Executing task: {task}")

        # Report start
        self.report_status("started", {"task": task})

        try:
            # Execute based on task type
            result = self._do_work(task)

            # Report completion
            self.report_status("completed", {"result": result})

            # Return result to manager
            return self.orchestrator.create_message(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                message_type=MessageType.REPORT,
                subject=f"Task Completed: {task.get('type', 'unknown')}",
                body={"result": result, "task_id": task.get('id')},
                parent_message_id=message.id
            )

        except Exception as e:
            self.logger.error(f"Task failed: {e}")
            self.report_status("failed", {"error": str(e)})
            return None

    def _do_work(self, task: Dict) -> Dict:
        """
        Perform the actual work. Override in specific subagent classes.
        """
        # Placeholder - actual implementation would call skills/tools
        return {"status": "completed", "message": "Work done"}


# ==========================================
# Agent Factory
# ==========================================
def create_agent(
    agent_type: str,
    config_path: str,
    orchestrator: AgentOrchestrator
) -> BaseAgent:
    """Factory function to create agents"""
    agent_classes = {
        "ceo": CEOAgent,
        "manager": ManagerAgent,
        "subagent": SubAgent
    }

    agent_class = agent_classes.get(agent_type.lower(), SubAgent)
    return agent_class(config_path, orchestrator)


# ==========================================
# Main Entry Point
# ==========================================
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run a Novel Empire Agent')
    parser.add_argument(
        'agent',
        choices=['ceo', 'claude-manager', 'n8n-manager',
                 'claude-writer', 'claude-quality',
                 'n8n-generator', 'n8n-writer', 'n8n-quality'],
        help='Agent to run'
    )
    parser.add_argument(
        '--base-dir',
        help='Base directory of the project'
    )
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Run as daemon'
    )

    args = parser.parse_args()

    # Determine base directory
    if args.base_dir:
        base_dir = Path(args.base_dir)
    else:
        base_dir = Path(__file__).parent.parent

    # Config file mapping
    config_mapping = {
        'ceo': 'config/ceo.yaml',
        'claude-manager': 'config/claude-manager.yaml',
        'n8n-manager': 'config/n8n-manager.yaml',
        'claude-writer': 'config/subagents/claude-writer.yaml',
        'claude-quality': 'config/subagents/claude-quality.yaml',
        'n8n-generator': 'config/subagents/n8n-generator.yaml',
        'n8n-writer': 'config/subagents/n8n-writer.yaml',
        'n8n-quality': 'config/subagents/n8n-quality.yaml'
    }

    # Agent type mapping
    type_mapping = {
        'ceo': 'ceo',
        'claude-manager': 'manager',
        'n8n-manager': 'manager',
        'claude-writer': 'subagent',
        'claude-quality': 'subagent',
        'n8n-generator': 'subagent',
        'n8n-writer': 'subagent',
        'n8n-quality': 'subagent'
    }

    # Setup
    agents_dir = base_dir / "agents"
    config_path = agents_dir / config_mapping[args.agent]
    agent_type = type_mapping[args.agent]

    # Create orchestrator
    orchestrator = AgentOrchestrator(str(base_dir))

    # Create and run agent
    agent = create_agent(agent_type, str(config_path), orchestrator)

    print(f"Starting {agent.agent_name}...")
    print("Press Ctrl+C to stop")

    agent.start()


if __name__ == "__main__":
    main()
