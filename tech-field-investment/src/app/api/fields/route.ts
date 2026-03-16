import { NextResponse } from "next/server";
import { TECH_FIELDS } from "@/lib/mock-data";

/**
 * GET /api/fields
 * Returns the list of available tech fields.
 */
export async function GET() {
  return NextResponse.json({ fields: TECH_FIELDS });
}
