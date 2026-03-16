"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import {
  TECH_FIELDS,
  getInvestmentData,
  getFieldSummary,
} from "@/lib/mock-data";
import InvestmentChart from "@/components/InvestmentChart";
import Link from "next/link";

export default function DashboardPage() {
  const [fieldIds, setFieldIds] = useState<string[]>([]);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();

      if (!user) {
        router.push("/auth/login");
        return;
      }

      setUserEmail(user.email ?? null);

      // Load selected fields from Supabase
      const { data } = await supabase
        .from("user_fields")
        .select("field_id")
        .eq("user_id", user.id);

      if (data && data.length > 0) {
        setFieldIds(data.map((r) => r.field_id));
      } else {
        // No fields selected yet — redirect to selection
        router.push("/fields");
        return;
      }

      setLoading(false);
    }
    load();
  }, [router]);

  async function handleLogout() {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push("/");
    router.refresh();
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-400">読み込み中...</p>
      </div>
    );
  }

  const chartData = getInvestmentData(fieldIds);

  return (
    <div className="min-h-screen px-4 py-8">
      {/* Header */}
      <div className="mx-auto mb-8 flex max-w-6xl items-center justify-between">
        <h1 className="text-2xl font-bold text-white">
          Investment Dashboard
        </h1>
        <div className="flex items-center gap-4">
          {userEmail && (
            <span className="text-sm text-gray-400">{userEmail}</span>
          )}
          <Link
            href="/fields"
            className="rounded-lg border border-gray-600 px-4 py-2 text-sm text-gray-300 transition hover:border-gray-400"
          >
            分野を変更
          </Link>
          <button
            onClick={handleLogout}
            className="rounded-lg border border-gray-600 px-4 py-2 text-sm text-gray-300 transition hover:border-red-400 hover:text-red-400"
          >
            ログアウト
          </button>
        </div>
      </div>

      <div className="mx-auto max-w-6xl space-y-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {fieldIds.map((id) => {
            const field = TECH_FIELDS.find((f) => f.id === id);
            const summary = getFieldSummary(id);
            const isPositive = summary.change >= 0;
            return (
              <div
                key={id}
                className="rounded-xl border border-gray-800 bg-gray-900 p-5"
              >
                <div className="mb-2 flex items-center gap-2">
                  <span className="text-xl">{field?.icon}</span>
                  <span className="text-sm font-medium text-gray-300">
                    {field?.label}
                  </span>
                </div>
                <p className="text-2xl font-bold text-white">
                  ${summary.latest}B
                </p>
                <p
                  className={`mt-1 text-sm font-medium ${
                    isPositive ? "text-green-400" : "text-red-400"
                  }`}
                >
                  {isPositive ? "+" : ""}
                  {summary.change.toFixed(1)}% vs 前四半期
                </p>
              </div>
            );
          })}
        </div>

        {/* Chart */}
        <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
          <h2 className="mb-4 text-lg font-semibold text-white">
            VC投資トレンド（四半期別）
          </h2>
          {fieldIds.length > 0 ? (
            <InvestmentChart data={chartData} fieldIds={fieldIds} />
          ) : (
            <p className="py-12 text-center text-gray-500">
              分野を選択してください
            </p>
          )}
          <p className="mt-4 text-right text-xs text-gray-600">
            * 現在は仮データを表示中。APIエンドポイント接続後にリアルデータに切り替わります。
          </p>
        </div>
      </div>
    </div>
  );
}
