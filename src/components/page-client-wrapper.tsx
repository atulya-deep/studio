'use client';

import * as React from 'react';
import { addDays } from 'date-fns';
import type { DateRange } from 'react-day-picker';
import { Presentation } from 'lucide-react';

import { DateRangePicker } from '@/components/date-range-picker';

export function PageClientWrapper({ children }: { children: React.ReactNode }) {
  const [date, setDate] = React.useState<DateRange | undefined>({
    from: addDays(new Date(), -30),
    to: new Date(),
  });

  return (
    <div className="flex flex-col min-h-screen">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <Presentation className="h-6 w-6 text-primary" />
            <h1 className="text-xl font-bold">MarketVerse</h1>
          </div>
          <DateRangePicker date={date} setDate={setDate} />
        </div>
      </header>
      <main className="flex-1 container py-8">
        {React.cloneElement(children as React.ReactElement, { dateRange: date })}
      </main>
    </div>
  );
}
