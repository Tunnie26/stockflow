export default function DashboardLoading() {
  return (
    <>
      <div className="space-y-2">
        <div className="h-7 w-40 animate-pulse rounded-md bg-[#18253A]" />
        <div className="h-4 w-72 animate-pulse rounded-md bg-[#111A2A]" />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <div
            key={index}
            className="h-[145px] animate-pulse rounded-[14px] border border-[#202C43] bg-[#0D1422]"
          />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
        {Array.from({ length: 2 }).map((_, index) => (
          <div
            key={index}
            className="h-[320px] animate-pulse rounded-[14px] border border-[#202C43] bg-[#0D1422]"
          />
        ))}
      </div>
    </>
  );
}