"""
Novel Factory - Formatting Helpers
Color utilities และ formatting helpers สำหรับ Google Sheets
"""

import config
from typing import Dict, List, Optional


def hex_to_rgb(hex_color: str) -> Dict[str, float]:
    """
    Convert hex color to RGB (0.0-1.0 range for Google Sheets)

    Args:
        hex_color: Hex color string (e.g., "#F59E0B")

    Returns:
        dict: {"red": float, "green": float, "blue": float}
    """
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return {
        "red": r / 255.0,
        "green": g / 255.0,
        "blue": b / 255.0
    }


def create_cell_format(
    bg_color: Optional[Dict] = None,
    text_color: Optional[Dict] = None,
    bold: bool = False,
    font_size: int = 10,
    horizontal_alignment: str = "LEFT",
    vertical_alignment: str = "MIDDLE"
) -> Dict:
    """
    Create cell format object for Google Sheets

    Args:
        bg_color: Background color {"red": float, "green": float, "blue": float}
        text_color: Text color
        bold: Bold text
        font_size: Font size
        horizontal_alignment: "LEFT", "CENTER", "RIGHT"
        vertical_alignment: "TOP", "MIDDLE", "BOTTOM"

    Returns:
        dict: Cell format for batch_update
    """
    format_obj = {
        "textFormat": {
            "bold": bold,
            "fontSize": font_size
        },
        "horizontalAlignment": horizontal_alignment,
        "verticalAlignment": vertical_alignment
    }

    if bg_color:
        format_obj["backgroundColor"] = bg_color

    if text_color:
        format_obj["textFormat"]["foregroundColor"] = text_color

    return format_obj


def create_header_format() -> Dict:
    """
    Create standard header format

    Returns:
        dict: Header cell format
    """
    return create_cell_format(
        bg_color={"red": 0.2, "green": 0.2, "blue": 0.2},  # Dark gray
        text_color={"red": 1.0, "green": 1.0, "blue": 1.0},  # White
        bold=True,
        font_size=11,
        horizontal_alignment="CENTER"
    )


def create_platform_cell_batch(
    spreadsheet_id: str,
    sheet_id: int,
    row: int,
    start_col: int,
    chapters: List[bool],
    platform_color: Dict,
    published_opacity: float = 1.0,
    unpublished_opacity: float = 0.3
) -> List[Dict]:
    """
    Create batch update requests for platform Gantt row

    Args:
        spreadsheet_id: Spreadsheet ID
        sheet_id: Sheet ID
        row: Row number (0-indexed)
        start_col: Starting column (0-indexed)
        chapters: List of booleans (True=published, False=not published)
        platform_color: Base platform color
        published_opacity: Opacity for published chapters (1.0 = solid)
        unpublished_opacity: Opacity for unpublished chapters (0.3 = light)

    Returns:
        list: List of batch update request objects
    """
    requests = []

    for idx, published in enumerate(chapters):
        col = start_col + idx

        # Calculate color with opacity
        if published:
            color = {
                "red": platform_color["red"],
                "green": platform_color["green"],
                "blue": platform_color["blue"],
                "alpha": published_opacity
            }
        else:
            color = {
                "red": platform_color["red"],
                "green": platform_color["green"],
                "blue": platform_color["blue"],
                "alpha": unpublished_opacity
            }

        # Create update request
        requests.append({
            "updateCells": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row,
                    "endRowIndex": row + 1,
                    "startColumnIndex": col,
                    "endColumnIndex": col + 1
                },
                "rows": [{
                    "values": [{
                        "userEnteredFormat": {
                            "backgroundColor": color
                        }
                    }]
                }],
                "fields": "userEnteredFormat.backgroundColor"
            }
        })

    return requests


def create_status_format(status: str) -> Dict:
    """
    Create cell format for status column

    Args:
        status: Status text (e.g., "กำลังผลิต")

    Returns:
        dict: Cell format
    """
    color = config.get_status_color(status)

    return create_cell_format(
        bg_color=color,
        text_color={"red": 0.0, "green": 0.0, "blue": 0.0},  # Black text
        bold=True,
        horizontal_alignment="CENTER"
    )


def create_border_request(
    sheet_id: int,
    start_row: int,
    end_row: int,
    start_col: int,
    end_col: int,
    border_style: str = "SOLID",
    border_color: Optional[Dict] = None
) -> Dict:
    """
    Create border update request

    Args:
        sheet_id: Sheet ID
        start_row: Start row (0-indexed)
        end_row: End row (exclusive)
        start_col: Start column (0-indexed)
        end_col: End column (exclusive)
        border_style: "SOLID", "DOTTED", "DASHED"
        border_color: Border color (default: black)

    Returns:
        dict: Border update request
    """
    if not border_color:
        border_color = {"red": 0.0, "green": 0.0, "blue": 0.0}

    border = {
        "style": border_style,
        "width": 1,
        "color": border_color
    }

    return {
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "top": border,
            "bottom": border,
            "left": border,
            "right": border,
            "innerHorizontal": border,
            "innerVertical": border
        }
    }


def create_auto_filter_request(sheet_id: int, start_row: int, end_row: int, start_col: int, end_col: int) -> Dict:
    """
    Create auto-filter request

    Args:
        sheet_id: Sheet ID
        start_row: Start row (0-indexed)
        end_row: End row (exclusive)
        start_col: Start column (0-indexed)
        end_col: End column (exclusive)

    Returns:
        dict: Auto-filter request
    """
    return {
        "setBasicFilter": {
            "filter": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": start_row,
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col,
                    "endColumnIndex": end_col
                }
            }
        }
    }


def create_freeze_request(sheet_id: int, frozen_row_count: int = 0, frozen_column_count: int = 0) -> Dict:
    """
    Create freeze rows/columns request

    Args:
        sheet_id: Sheet ID
        frozen_row_count: Number of rows to freeze from top
        frozen_column_count: Number of columns to freeze from left

    Returns:
        dict: Freeze request
    """
    return {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": frozen_row_count,
                    "frozenColumnCount": frozen_column_count
                }
            },
            "fields": "gridProperties(frozenRowCount,frozenColumnCount)"
        }
    }


def create_merge_cells_request(sheet_id: int, start_row: int, end_row: int, start_col: int, end_col: int) -> Dict:
    """
    Create merge cells request

    Args:
        sheet_id: Sheet ID
        start_row: Start row (0-indexed)
        end_row: End row (exclusive)
        start_col: Start column (0-indexed)
        end_col: End column (exclusive)

    Returns:
        dict: Merge cells request
    """
    return {
        "mergeCells": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "mergeType": "MERGE_ALL"
        }
    }


def create_column_width_request(sheet_id: int, start_col: int, end_col: int, pixel_size: int) -> Dict:
    """
    Create column width update request

    Args:
        sheet_id: Sheet ID
        start_col: Start column (0-indexed)
        end_col: End column (exclusive)
        pixel_size: Width in pixels

    Returns:
        dict: Column width request
    """
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": start_col,
                "endIndex": end_col
            },
            "properties": {
                "pixelSize": pixel_size
            },
            "fields": "pixelSize"
        }
    }


def create_row_height_request(sheet_id: int, start_row: int, end_row: int, pixel_size: int) -> Dict:
    """
    Create row height update request

    Args:
        sheet_id: Sheet ID
        start_row: Start row (0-indexed)
        end_row: End row (exclusive)
        pixel_size: Height in pixels

    Returns:
        dict: Row height request
    """
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start_row,
                "endIndex": end_row
            },
            "properties": {
                "pixelSize": pixel_size
            },
            "fields": "pixelSize"
        }
    }
