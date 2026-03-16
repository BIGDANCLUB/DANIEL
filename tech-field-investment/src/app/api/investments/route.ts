import { NextRequest, NextResponse } from "next/server";
import { getInvestmentData, TECH_FIELDS } from "@/lib/mock-data";

/**
 * GET /api/investments?fields=ai,quantum,biotech
 *
 * Placeholder endpoint — currently returns mock data.
 * Replace the data source with a real API (PitchBook, Crunchbase, etc.)
 * when ready.
 */
export async function GET(request: NextRequest) {
  const fieldsParam = request.nextUrl.searchParams.get("fields");

  if (!fieldsParam) {
    return NextResponse.json(
      { error: "Missing 'fields' query parameter. Example: ?fields=ai,quantum" },
      { status: 400 }
    );
  }

  const fieldIds = fieldsParam.split(",").filter(Boolean);
  const validIds = TECH_FIELDS.map((f) => f.id);
  const invalid = fieldIds.filter((id) => !validIds.includes(id as typeof validIds[number]));

  if (invalid.length > 0) {
    return NextResponse.json(
      {
        error: `Invalid field IDs: ${invalid.join(", ")}`,
        valid: validIds,
      },
      { status: 400 }
    );
  }

  // TODO: Replace with real data source
  const data = getInvestmentData(fieldIds);

  return NextResponse.json({
    source: "mock",
    fields: fieldIds,
    data,
  });
}

/**
 * POST /api/investments
 *
 * Placeholder for ingesting investment data from external sources.
 * Body: { field: string, quarter: string, amount: number }
 */
export async function POST(request: NextRequest) {
  const body = await request.json();

  // TODO: Validate and store in Supabase
  // const supabase = await createClient();
  // await supabase.from('investments').insert(body);

  return NextResponse.json({
    message: "Data ingestion endpoint (placeholder). Not yet connected to database.",
    received: body,
  });
}
