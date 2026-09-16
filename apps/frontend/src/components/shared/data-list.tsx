import { cn } from "@/lib/utils";

interface DataListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor?: (item: T, index: number) => React.Key;
  emptyState?: React.ReactNode;
  className?: string;
}

export function DataList<T>({
  items,
  renderItem,
  keyExtractor,
  emptyState,
  className,
}: DataListProps<T>) {
  if (items.length === 0) {
    return emptyState ?? null;
  }

  return (
    <div className={cn("space-y-3", className)}>
      {items.map((item, index) => {
        const key = keyExtractor ? keyExtractor(item, index) : index;

        return <div key={key}>{renderItem(item, index)}</div>;
      })}
    </div>
  );
}
