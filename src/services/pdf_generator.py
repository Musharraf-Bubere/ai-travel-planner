from io import BytesIO
from typing import Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def generate_travel_plan_pdf(
    destination: str,
    travel_dates: str,
    trip_details: dict[str, Any],
) -> bytes:
    """
    Generate a downloadable PDF travel plan.

    The PDF is generated in memory and returned as bytes.
    No temporary file is created.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "AI Travel Planner",
            title_style,
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * inch,
        )
    )

    story.append(
        Paragraph(
            f"<b>Destination:</b> {destination}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Travel Dates:</b> {travel_dates}",
            body_style,
        )
    )

    story.append(
        Spacer(
            1,
            0.2 * inch,
        )
    )

    # ---------------------------------------------------------
    # Trip Summary
    # ---------------------------------------------------------

    trip_summary = trip_details.get(
        "trip_summary"
    )

    if trip_summary:
        story.append(
            Paragraph(
                "Trip Summary",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                str(trip_summary),
                body_style,
            )
        )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

    # ---------------------------------------------------------
    # Itinerary
    # ---------------------------------------------------------

    itinerary_data = trip_details.get(
        "itinerary",
        [],
    )

    if isinstance(itinerary_data, dict):
        itinerary = itinerary_data.get(
            "itinerary",
            [],
        )
    else:
        itinerary = itinerary_data

    if itinerary:
        story.append(
            Paragraph(
                "Itinerary",
                heading_style,
            )
        )

        for item in itinerary:
            day = item.get(
                "day",
                "",
            )

            time = item.get(
                "time",
                "",
            )

            activity = item.get(
                "activity",
                "",
            )

            location = item.get(
                "location",
                "",
            )

            description = item.get(
                "description",
                "",
            )

            story.append(
                Paragraph(
                    f"<b>Day {day} — {time}</b>",
                    body_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>{activity}</b>",
                    body_style,
                )
            )

            if location:
                story.append(
                    Paragraph(
                        f"<b>Location:</b> {location}",
                        body_style,
                    )
                )

            if description:
                story.append(
                    Paragraph(
                        str(description),
                        body_style,
                    )
                )

            story.append(
                Spacer(
                    1,
                    0.12 * inch,
                )
            )

    # ---------------------------------------------------------
    # Accommodation
    # ---------------------------------------------------------

    accommodation_summary = trip_details.get(
        "accommodation_summary"
    )

    if accommodation_summary:
        story.append(
            Paragraph(
                "Accommodation",
                heading_style,
            )
        )

        if isinstance(
            accommodation_summary,
            dict,
        ):
            recommendation = accommodation_summary.get(
                "stay_recommendation"
            )

            budget_assessment = accommodation_summary.get(
                "budget_assessment"
            )

            if recommendation:
                story.append(
                    Paragraph(
                        f"<b>Recommendation:</b> "
                        f"{recommendation}",
                        body_style,
                    )
                )

            if budget_assessment:
                story.append(
                    Paragraph(
                        f"<b>Budget:</b> "
                        f"{budget_assessment}",
                        body_style,
                    )
                )

        else:
            story.append(
                Paragraph(
                    str(accommodation_summary),
                    body_style,
                )
            )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

    # ---------------------------------------------------------
    # Food
    # ---------------------------------------------------------

    food_summary = trip_details.get(
        "food_summary"
    )

    if food_summary:
        story.append(
            Paragraph(
                "Food Recommendations",
                heading_style,
            )
        )

        if isinstance(
            food_summary,
            dict,
        ):
            recommendation = food_summary.get(
                "food_recommendation"
            )

            budget_assessment = food_summary.get(
                "budget_assessment"
            )

            if recommendation:
                story.append(
                    Paragraph(
                        f"<b>Recommendation:</b> "
                        f"{recommendation}",
                        body_style,
                    )
                )

            if budget_assessment:
                story.append(
                    Paragraph(
                        f"<b>Budget:</b> "
                        f"{budget_assessment}",
                        body_style,
                    )
                )

        else:
            story.append(
                Paragraph(
                    str(food_summary),
                    body_style,
                )
            )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

    # ---------------------------------------------------------
    # Travel Tips
    # ---------------------------------------------------------

    travel_tips = trip_details.get(
        "travel_tips",
        [],
    )

    if travel_tips:
        story.append(
            Paragraph(
                "Travel Tips",
                heading_style,
            )
        )

        if isinstance(
            travel_tips,
            list,
        ):
            for tip in travel_tips:
                story.append(
                    Paragraph(
                        f"• {tip}",
                        body_style,
                    )
                )

        else:
            story.append(
                Paragraph(
                    str(travel_tips),
                    body_style,
                )
            )

        story.append(
            Spacer(
                1,
                0.15 * inch,
            )
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    validation = trip_details.get(
        "validation",
        {},
    )

    if validation:
        story.append(
            Paragraph(
                "Itinerary Validation",
                heading_style,
            )
        )

        is_valid = validation.get(
            "is_valid"
        )

        feedback = validation.get(
            "feedback"
        )

        story.append(
            Paragraph(
                f"<b>Valid:</b> {is_valid}",
                body_style,
            )
        )

        if feedback:
            story.append(
                Paragraph(
                    f"<b>Feedback:</b> {feedback}",
                    body_style,
                )
            )

    # ---------------------------------------------------------
    # Build PDF
    # ---------------------------------------------------------

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()