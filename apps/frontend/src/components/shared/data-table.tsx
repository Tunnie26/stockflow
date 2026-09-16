import { cn } from "@/lib/utils";

export interface DataTableColumn<T> {
  key: string;
  header: React.ReactNode;
  render: (item: T, index: number) => React.ReactNode;
  className?: string;
  headerClassName?: string;
}

interface DataTableProps<T> {
  data: T[];
  columns: DataTableColumn<T>[];
  keyExtractor?: (item: T, index: number) => React.Key;
  emptyState?: React.ReactNode;
  className?: string;
}

export function DataTable<T>({
  data,
  columns,
  keyExtractor,
  emptyState,
  className,
}: DataTableProps<T>) {
  if (data.length === 0) {
    return emptyState ?? null;
  }

  return (
    <div
      className={cn(
        "overflow-hidden rounded-xl border border-[#202C43]",
        className,
      )}
    >
      <div className="data-table-scroll overflow-x-auto">
        <table className="w-full min-w-[640px] border-collapse">
          <thead>
            <tr className="border-b border-[#202C43] bg-[#090E1A]">
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={cn(
                    "px-4 py-3 text-left text-xs font-medium uppercase tracking-wide text-[#8490A8]",
                    column.headerClassName,
                  )}
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {data.map((item, index) => {
              const key = keyExtractor ? keyExtractor(item, index) : index;

              return (
                <tr
                  key={key}
                  className="border-b border-[#172136] last:border-b-0 hover:bg-[rgba(79,124,255,0.04)]"
                >
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className={cn(
                        "px-4 py-3 text-sm text-[#B8C2D9]",
                        column.className,
                      )}
                    >
                      {column.render(item, index)}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
