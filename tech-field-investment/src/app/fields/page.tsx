"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createClient } from "@/lib/supabase/client";
import { TECH_FIELDS } from "@/lib/mock-data";

export default function FieldSelectionPage() {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const router = useRouter();

  // Load existing selections from Supabase
  useEffect(() => {
    async function load() {
      const supabase = createClient();
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) {
        setLoading(false);
        return;
      }

      const { data } = await supabase
        .from("user_fields")
        .select("field_id")
        .eq("user_id", user.id);

      if (data && data.length > 0) {
        setSelected(new Set(data.map((r) => r.field_id)));
      }
      setLoading(false);
    }
    load();
  }, []);

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  async function handleSubmit() {
    if (selected.size === 0) return;
    setSaving(true);

    const supabase = createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (user) {
      // Delete existing selections, then insert new ones
      await supabase.from("user_fields").delete().eq("user_id", user.id);
      await supabase.from("user_fields").insert(
        Array.from(selected).map((field_id) => ({
          user_id: user.id,
          field_id,
        }))
      );
    }

    router.push("/dashboard");
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-400">読み込み中...</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col items-center px-4 py-12">
      <div className="w-full max-w-3xl">
        <h1 className="mb-2 text-3xl font-bold text-white">
          注目分野を選択
        </h1>
        <p className="mb-8 text-gray-400">
          投資トレンドを追跡したい技術分野を選んでください（複数選択可）
        </p>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          {TECH_FIELDS.map((field) => {
            const isSelected = selected.has(field.id);
            return (
              <button
                key={field.id}
                onClick={() => toggle(field.id)}
                className={`flex items-center gap-3 rounded-xl border-2 px-5 py-4 text-left transition ${
                  isSelected
                    ? "border-blue-500 bg-blue-500/10 text-white"
                    : "border-gray-700 bg-gray-900 text-gray-300 hover:border-gray-500"
                }`}
              >
                <span className="text-2xl">{field.icon}</span>
                <span className="font-medium">{field.label}</span>
                {isSelected && (
                  <span className="ml-auto text-blue-400">&#10003;</span>
                )}
              </button>
            );
          })}
        </div>

        <div className="mt-8 flex items-center justify-between">
          <p className="text-sm text-gray-500">
            {selected.size}件選択中
          </p>
          <button
            onClick={handleSubmit}
            disabled={selected.size === 0 || saving}
            className="rounded-lg bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {saving ? "保存中..." : "ダッシュボードへ"}
          </button>
        </div>
      </div>
    </div>
  );
}
