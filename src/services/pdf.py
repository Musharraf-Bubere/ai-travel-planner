from io import BytesIO
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.lib import colors


def _safe_text(value: Any) -> str:
    """Convert a value into readable PDF text."""
    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        return str(value)

    return str(value)


def generate_travel_plan_pdf(
    trip: Any,
    travel_plan: Any,
) -> BytesIO:
    """
    Generate a PDF document from a persisted Trip and TravelPlan.

    Returns:
        BytesIO: PDF content ready to be returned by FastAPI.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
        title="AI Travel Planner - Travel Plan",
        author="AI Travel Planner",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TravelPlanTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=28,
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "TravelPlanSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        leading=16,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "TravelPlanHeading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        spaceBefore=14,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "TravelPlanBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=6,
    )

    small_style = ParagraphStyle(
        "TravelPlanSmall",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=4,
    )

    story = []

    # ============================================================
    # TITLE
    # ============================================================

    story.append(
        Paragraph(
            "✈️ AI Travel Planner",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Multi-Agent Travel Planning System",
            subtitle_style,
        )
    )

    # ============================================================
    # TRIP SUMMARY
    # ============================================================

    story.append(
        Paragraph(
            "Trip Details",
            heading_style,
        )
    )

    trip_data = [
        ["Destination", _safe_text(trip.destination)],
        ["Travel Dates", _safe_text(trip.travel_dates)],
        ["Duration", f"{trip.duration} days"],
        ["Travelers", _safe_text(trip.travelers)],
        ["Budget", f"₹{trip.budget:,.2f}"],
        ["Status", _safe_text(trip.status)],
    ]

    trip_table = Table(
        trip_data,
        colWidths=[1.5 * inch, 4.8 * inch],
    )

    trip_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(trip_table)
    story.append(Spacer(1, 12))

    # ============================================================
    # ITINERARY
    # ============================================================

    itinerary = travel_plan.itinerary or {}

    story.append(
        Paragraph(
            "🗓️ Itinerary",
            heading_style,
        )
    )

    days = itinerary.get("itinerary", [])

    if days:

        for day in days:

            day_number = day.get(
                "day",
                "",
            )

            time = day.get(
                "time",
                "",
            )

            activity = day.get(
                "activity",
                "",
            )

            location = day.get(
                "location",
                "",
            )

            description = day.get(
                "description",
                "",
            )

            day_content = [
                Paragraph(
                    f"<b>Day {day_number} — {_safe_text(time)}</b>",
                    body_style,
                ),
                Paragraph(
                    f"<b>Activity:</b> {_safe_text(activity)}",
                    body_style,
                ),
                Paragraph(
                    f"<b>Location:</b> {_safe_text(location)}",
                    body_style,
                ),
                Paragraph(
                    f"<b>Description:</b> {_safe_text(description)}",
                    body_style,
                ),
            ]

            story.append(
                KeepTogether(day_content)
            )

            story.append(
                Spacer(1, 5)
            )

    else:
        story.append(
            Paragraph(
                "No itinerary details available.",
                body_style,
            )
        )

    # ============================================================
    # PLANNING NOTES
    # ============================================================

    planning_notes = itinerary.get(
        "planning_notes",
        [],
    )

    if planning_notes:

        story.append(
            Paragraph(
                "📝 Planning Notes",
                heading_style,
            )
        )

        for note in planning_notes:
            story.append(
                Paragraph(
                    f"• {_safe_text(note)}",
                    body_style,
                )
            )

    # ============================================================
    # ACCOMMODATION
    # ============================================================

    accommodation = (
        travel_plan.accommodation_summary
        or {}
    )

    story.append(
        Paragraph(
            "🏨 Accommodation",
            heading_style,
        )
    )

    recommended_area = accommodation.get(
        "recommended_area"
    )

    if recommended_area:
        story.append(
            Paragraph(
                f"<b>Recommended Area:</b> "
                f"{_safe_text(recommended_area)}",
                body_style,
            )
        )

    stay_recommendation = accommodation.get(
        "stay_recommendation"
    )

    if stay_recommendation:
        story.append(
            Paragraph(
                f"<b>Recommendation:</b> "
                f"{_safe_text(stay_recommendation)}",
                body_style,
            )
        )

    accommodation_budget = accommodation.get(
        "budget_assessment"
    )

    if accommodation_budget:
        story.append(
            Paragraph(
                f"<b>Budget Assessment:</b> "
                f"{_safe_text(accommodation_budget)}",
                body_style,
            )
        )

    accommodation_options = accommodation.get(
        "accommodation_options",
        [],
    )

    if accommodation_options:

        accommodation_data = [
            [
                "Name",
                "Rating",
                "Price/Night",
            ]
        ]

        for option in accommodation_options:

            accommodation_data.append(
                [
                    _safe_text(
                        option.get("name")
                    ),
                    _safe_text(
                        option.get("rating")
                    ),
                    (
                        f"₹{option.get('price_per_night', 0):,.2f}"
                    ),
                ]
            )

        accommodation_table = Table(
            accommodation_data,
            colWidths=[
                3.5 * inch,
                1 * inch,
                1.5 * inch,
            ],
            repeatRows=1,
        )

        accommodation_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            )
        )

        story.append(
            accommodation_table
        )

    # ============================================================
    # FOOD
    # ============================================================

    food = (
        travel_plan.food_summary
        or {}
    )

    story.append(
        Paragraph(
            "🍴 Food & Restaurants",
            heading_style,
        )
    )

    food_recommendation = food.get(
        "food_recommendation"
    )

    if food_recommendation:
        story.append(
            Paragraph(
                f"<b>Recommendation:</b> "
                f"{_safe_text(food_recommendation)}",
                body_style,
            )
        )

    food_budget = food.get(
        "budget_assessment"
    )

    if food_budget:
        story.append(
            Paragraph(
                f"<b>Budget Assessment:</b> "
                f"{_safe_text(food_budget)}",
                body_style,
            )
        )

    restaurants = food.get(
        "recommended_restaurants",
        [],
    )

    if restaurants:

        restaurant_data = [
            [
                "Restaurant",
                "Rating",
                "Category",
            ]
        ]

        for restaurant in restaurants:

            restaurant_data.append(
                [
                    _safe_text(
                        restaurant.get("name")
                    ),
                    _safe_text(
                        restaurant.get("rating")
                    ),
                    _safe_text(
                        restaurant.get("category")
                    ),
                ]
            )

        restaurant_table = Table(
            restaurant_data,
            colWidths=[
                3 * inch,
                1 * inch,
                2 * inch,
            ],
            repeatRows=1,
        )

        restaurant_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9,
                    ),
                ]
            )
        )

        story.append(
            restaurant_table
        )

    # ============================================================
    # TRAVEL TIPS
    # ============================================================

    travel_tips = (
        travel_plan.travel_tips
        or []
    )

    story.append(
        Paragraph(
            "💡 Travel Tips",
            heading_style,
        )
    )

    if isinstance(travel_tips, list):

        for tip in travel_tips:
            story.append(
                Paragraph(
                    f"• {_safe_text(tip)}",
                    body_style,
                )
            )

    else:
        story.append(
            Paragraph(
                _safe_text(travel_tips),
                body_style,
            )
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    validation = (
        travel_plan.validation
        or {}
    )

    story.append(
        Paragraph(
            "🔍 Validation",
            heading_style,
        )
    )

    validation_status = validation.get(
        "is_valid",
        False,
    )

    story.append(
        Paragraph(
            f"<b>Status:</b> "
            f"{'Valid' if validation_status else 'Invalid'}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Validation Attempts:</b> "
            f"{travel_plan.validation_attempts}",
            body_style,
        )
    )

    validation_feedback = validation.get(
        "feedback"
    )

    if validation_feedback:
        story.append(
            Paragraph(
                f"<b>Feedback:</b> "
                f"{_safe_text(validation_feedback)}",
                body_style,
            )
        )

    issues = validation.get(
        "issues",
        [],
    )

    if issues:

        story.append(
            Paragraph(
                "<b>Issues:</b>",
                body_style,
            )
        )

        for issue in issues:
            story.append(
                Paragraph(
                    f"• {_safe_text(issue)}",
                    small_style,
                )
            )

    # ============================================================
    # FOOTER
    # ============================================================

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Generated by AI Travel Planner",
            subtitle_style,
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer