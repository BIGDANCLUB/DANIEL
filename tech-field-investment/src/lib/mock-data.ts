export const TECH_FIELDS = [
  { id: "ai", label: "AI / Machine Learning", icon: "🤖" },
  { id: "quantum", label: "Quantum Computing", icon: "⚛️" },
  { id: "biotech", label: "Biotechnology", icon: "🧬" },
  { id: "cleantech", label: "Clean Energy / CleanTech", icon: "🌱" },
  { id: "fintech", label: "FinTech", icon: "💳" },
  { id: "cybersecurity", label: "Cybersecurity", icon: "🔒" },
  { id: "space", label: "Space Tech", icon: "🚀" },
  { id: "robotics", label: "Robotics", icon: "🦾" },
  { id: "ar_vr", label: "AR / VR / Metaverse", icon: "🥽" },
  { id: "web3", label: "Web3 / Blockchain", icon: "⛓️" },
] as const;

export type FieldId = (typeof TECH_FIELDS)[number]["id"];

// Mock VC investment data (billions USD) — will be replaced by real API
export function getInvestmentData(fieldIds: string[]) {
  const quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Q1 2026"];

  const baseValues: Record<string, number[]> = {
    ai: [18.2, 22.5, 28.1, 35.0, 42.3],
    quantum: [1.2, 1.5, 1.8, 2.4, 3.1],
    biotech: [8.5, 9.2, 10.1, 11.3, 12.8],
    cleantech: [6.3, 7.8, 9.5, 11.2, 13.0],
    fintech: [12.1, 11.8, 13.2, 14.5, 15.1],
    cybersecurity: [5.4, 6.1, 7.3, 8.0, 9.2],
    space: [2.8, 3.2, 3.9, 4.5, 5.1],
    robotics: [3.1, 3.8, 4.5, 5.2, 6.0],
    ar_vr: [4.2, 3.8, 4.1, 5.0, 5.8],
    web3: [7.5, 5.2, 4.8, 6.1, 7.0],
  };

  return quarters.map((quarter, i) => {
    const point: Record<string, string | number> = { quarter };
    for (const id of fieldIds) {
      point[id] = baseValues[id]?.[i] ?? 0;
    }
    return point;
  });
}

export function getFieldSummary(fieldId: string) {
  const data = getInvestmentData([fieldId]);
  const latest = data[data.length - 1][fieldId] as number;
  const previous = data[data.length - 2][fieldId] as number;
  const change = ((latest - previous) / previous) * 100;
  return { latest, change };
}
