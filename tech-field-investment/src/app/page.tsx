import Link from "next/link";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <div className="max-w-2xl text-center">
        <h1 className="mb-4 text-5xl font-bold tracking-tight text-white">
          Tech Field
          <span className="text-blue-400"> Investment Tracker</span>
        </h1>
        <p className="mb-8 text-lg text-gray-400">
          AI、量子コンピューティング、バイオテクノロジーなど、
          注目分野のVC投資トレンドをリアルタイムに追跡
        </p>
        <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
          <Link
            href="/auth/login"
            className="rounded-lg bg-blue-600 px-8 py-3 font-semibold text-white transition hover:bg-blue-500"
          >
            ログイン
          </Link>
          <Link
            href="/auth/signup"
            className="rounded-lg border border-gray-600 px-8 py-3 font-semibold text-gray-300 transition hover:border-gray-400 hover:text-white"
          >
            新規登録
          </Link>
        </div>
      </div>
    </div>
  );
}
