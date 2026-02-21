#!/usr/bin/env python3
"""
Novel Empire Agent Orchestrator
จัดการการสื่อสารและ coordination ระหว่าง agents
"""

import os
import json
import yaml
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    TASK = "task"
    STATUS = "status"
    QUESTION = "question"
    REPORT = "report"
    ALERT = "alert"
    BROADCAST = "broadcast"


class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class Message:
    """Message structure for inter-agent communication"""
    id: str
    timestamp: str
    from_agent: str
    to_agent: str
    message_type: str
    priority: str
    subject: str
    body: Dict[str, Any]
    requires_response: bool = False
    deadline: Optional[str] = None
    parent_message_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        return cls(**data)


class AgentOrchestrator:
    """
    Central orchestrator for the Novel Empire agent system.
    Manages message routing, agent coordination, and system state.
    """

    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).parent.parent

        self.agents_dir = self.base_dir / "agents"
        self.config_dir = self.agents_dir / "config"
        self.messages_dir = self.agents_dir / "messages"
        self.logs_dir = self.agents_dir / "logs"

        # Load agent configurations
        self.agents = self._load_all_agents()

        # Message queues (in-memory for speed, persisted to disk)
        self.message_queues: Dict[str, List[Message]] = {}
        self._init_queues()

    def _load_all_agents(self) -> Dict[str, Dict]:
        """Load all agent configurations"""
        agents = {}

        # Load CEO
        ceo_config = self.config_dir / "ceo.yaml"
        if ceo_config.exists():
            with open(ceo_config, 'r', encoding='utf-8') as f:
                agents['ceo-001'] = yaml.safe_load(f)

        # Load Managers
        for manager_file in ['claude-manager.yaml', 'n8n-manager.yaml']:
            manager_path = self.config_dir / manager_file
            if manager_path.exists():
                with open(manager_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    agents[config['agent']['id']] = config

        # Load Subagents
        subagents_dir = self.config_dir / "subagents"
        if subagents_dir.exists():
            for subagent_file in subagents_dir.glob("*.yaml"):
                with open(subagent_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    agents[config['agent']['id']] = config

        return agents

    def _init_queues(self):
        """Initialize message queues for all agents"""
        for agent_id in self.agents:
            self.message_queues[agent_id] = []

        # Load persisted messages
        self._load_persisted_messages()

    def _load_persisted_messages(self):
        """Load messages from disk"""
        inbox_mapping = {
            'ceo-001': 'ceo-inbox',
            'mgr-claude-001': 'claude-manager',
            'mgr-n8n-001': 'n8n-manager'
        }

        for agent_id, inbox_name in inbox_mapping.items():
            inbox_path = self.messages_dir / inbox_name
            if inbox_path.exists():
                for msg_file in inbox_path.glob("*.json"):
                    try:
                        with open(msg_file, 'r', encoding='utf-8') as f:
                            msg_data = json.load(f)
                            self.message_queues[agent_id].append(
                                Message.from_dict(msg_data)
                            )
                    except Exception as e:
                        print(f"Error loading message {msg_file}: {e}")

    def create_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: MessageType,
        subject: str,
        body: Dict[str, Any],
        priority: Priority = Priority.NORMAL,
        requires_response: bool = False,
        deadline: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ) -> Message:
        """Create a new message"""
        return Message(
            id=f"msg-{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now().isoformat(),
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type.value,
            priority=priority.value,
            subject=subject,
            body=body,
            requires_response=requires_response,
            deadline=deadline,
            parent_message_id=parent_message_id
        )

    def send_message(self, message: Message) -> bool:
        """Send a message to an agent"""
        to_agent = message.to_agent

        # Validate recipient exists
        if to_agent not in self.agents and to_agent != "broadcast":
            print(f"Unknown agent: {to_agent}")
            return False

        # Handle broadcast
        if to_agent == "broadcast":
            return self._broadcast_message(message)

        # Add to queue
        if to_agent not in self.message_queues:
            self.message_queues[to_agent] = []

        self.message_queues[to_agent].append(message)

        # Persist to disk
        self._persist_message(message)

        # Log
        self._log_message(message, "SENT")

        return True

    def _broadcast_message(self, message: Message) -> bool:
        """Send message to all agents"""
        # Save to broadcasts folder
        broadcast_dir = self.messages_dir / "broadcasts"
        broadcast_dir.mkdir(exist_ok=True)

        filename = f"{message.id}.json"
        with open(broadcast_dir / filename, 'w', encoding='utf-8') as f:
            f.write(message.to_json())

        # Add to all queues
        for agent_id in self.agents:
            if agent_id != message.from_agent:
                self.message_queues[agent_id].append(message)

        self._log_message(message, "BROADCAST")
        return True

    def _persist_message(self, message: Message):
        """Save message to disk"""
        inbox_mapping = {
            'ceo-001': 'ceo-inbox',
            'mgr-claude-001': 'claude-manager',
            'mgr-n8n-001': 'n8n-manager'
        }

        to_agent = message.to_agent
        inbox_name = inbox_mapping.get(to_agent, to_agent)
        inbox_path = self.messages_dir / inbox_name
        inbox_path.mkdir(exist_ok=True)

        filename = f"{message.id}.json"
        with open(inbox_path / filename, 'w', encoding='utf-8') as f:
            f.write(message.to_json())

    def get_messages(
        self,
        agent_id: str,
        unread_only: bool = True,
        priority: Optional[Priority] = None
    ) -> List[Message]:
        """Get messages for an agent"""
        if agent_id not in self.message_queues:
            return []

        messages = self.message_queues[agent_id]

        if priority:
            messages = [m for m in messages if m.priority == priority.value]

        # Sort by priority and timestamp
        priority_order = {
            Priority.CRITICAL.value: 0,
            Priority.HIGH.value: 1,
            Priority.NORMAL.value: 2,
            Priority.LOW.value: 3
        }
        messages.sort(key=lambda m: (
            priority_order.get(m.priority, 2),
            m.timestamp
        ))

        return messages

    def acknowledge_message(self, message_id: str, agent_id: str):
        """Mark a message as read/processed"""
        if agent_id not in self.message_queues:
            return

        # Remove from queue
        self.message_queues[agent_id] = [
            m for m in self.message_queues[agent_id]
            if m.id != message_id
        ]

        # Move to archive
        self._archive_message(message_id, agent_id)

    def _archive_message(self, message_id: str, agent_id: str):
        """Move processed message to archive"""
        inbox_mapping = {
            'ceo-001': 'ceo-inbox',
            'mgr-claude-001': 'claude-manager',
            'mgr-n8n-001': 'n8n-manager'
        }

        inbox_name = inbox_mapping.get(agent_id, agent_id)
        source_path = self.messages_dir / inbox_name / f"{message_id}.json"
        archive_path = self.messages_dir / "archive" / f"{message_id}.json"

        if source_path.exists():
            archive_path.parent.mkdir(exist_ok=True)
            source_path.rename(archive_path)

    def _log_message(self, message: Message, action: str):
        """Log message activity"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "message_id": message.id,
            "from": message.from_agent,
            "to": message.to_agent,
            "type": message.message_type,
            "subject": message.subject
        }

        log_file = self.logs_dir / "orchestrator.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # ==========================================
    # Task Distribution Methods
    # ==========================================

    def assign_task_to_team(
        self,
        task: Dict[str, Any],
        team: str = "auto"
    ) -> str:
        """
        Assign a task to the appropriate team.
        Returns the assigned manager's ID.
        """
        if team == "auto":
            team = self._determine_best_team(task)

        manager_id = {
            "claude-code": "mgr-claude-001",
            "n8n": "mgr-n8n-001"
        }.get(team, "mgr-n8n-001")

        # Create task message
        message = self.create_message(
            from_agent="ceo-001",
            to_agent=manager_id,
            message_type=MessageType.TASK,
            subject=f"New Task: {task.get('title', 'Untitled')}",
            body=task,
            priority=Priority(task.get('priority', 'normal')),
            requires_response=True,
            deadline=task.get('deadline')
        )

        self.send_message(message)
        return manager_id

    def _determine_best_team(self, task: Dict[str, Any]) -> str:
        """Determine the best team for a task"""
        quality = task.get('quality', 'standard')
        count = task.get('novel_count', 1)
        mode = task.get('mode', 'single')

        if quality == 'premium' or quality == 'high':
            return "claude-code"
        elif count > 3 or mode == 'batch':
            return "n8n"
        elif count <= 3:
            return "claude-code"
        else:
            return "n8n"

    # ==========================================
    # Status and Reporting
    # ==========================================

    def get_system_status(self) -> Dict:
        """Get overall system status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "queues": {},
            "summary": {}
        }

        # Agent status
        for agent_id, config in self.agents.items():
            status["agents"][agent_id] = {
                "name": config['agent']['name'],
                "role": config['agent']['role'],
                "team": config['agent'].get('team', 'management'),
                "pending_messages": len(self.message_queues.get(agent_id, []))
            }

        # Queue summary
        total_messages = sum(
            len(q) for q in self.message_queues.values()
        )
        status["summary"] = {
            "total_agents": len(self.agents),
            "total_pending_messages": total_messages,
            "queues_with_messages": sum(
                1 for q in self.message_queues.values() if q
            )
        }

        return status

    def generate_daily_report(self) -> str:
        """Generate a daily status report"""
        status = self.get_system_status()

        report = f"""
# Novel Empire Daily Report
Generated: {status['timestamp']}

## System Status
- Total Agents: {status['summary']['total_agents']}
- Pending Messages: {status['summary']['total_pending_messages']}

## Agent Status
"""
        for agent_id, agent_status in status['agents'].items():
            report += f"""
### {agent_status['name']} ({agent_status['role']})
- Team: {agent_status['team']}
- Pending Messages: {agent_status['pending_messages']}
"""

        return report


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Novel Empire Agent Orchestrator'
    )
    parser.add_argument(
        '--base-dir',
        help='Base directory of the project'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate daily report'
    )
    parser.add_argument(
        '--send-task',
        type=str,
        help='Send a task (JSON string)'
    )

    args = parser.parse_args()

    orchestrator = AgentOrchestrator(args.base_dir)

    if args.status:
        status = orchestrator.get_system_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif args.report:
        report = orchestrator.generate_daily_report()
        print(report)

    elif args.send_task:
        task = json.loads(args.send_task)
        manager = orchestrator.assign_task_to_team(task)
        print(f"Task assigned to: {manager}")

    else:
        # Interactive mode
        print("Novel Empire Agent Orchestrator")
        print("================================")
        print("\nCommands:")
        print("  status  - Show system status")
        print("  report  - Generate daily report")
        print("  quit    - Exit")
        print()

        while True:
            try:
                cmd = input("orchestrator> ").strip().lower()

                if cmd == "status":
                    status = orchestrator.get_system_status()
                    print(json.dumps(status, ensure_ascii=False, indent=2))

                elif cmd == "report":
                    report = orchestrator.generate_daily_report()
                    print(report)

                elif cmd in ["quit", "exit", "q"]:
                    break

                else:
                    print(f"Unknown command: {cmd}")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break


if __name__ == "__main__":
    main()
