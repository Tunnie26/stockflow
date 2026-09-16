"use client";

import Image from "next/image";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import {
  defaultLanguage,
  languages,
} from "@/config/languages";

export function LanguageSelector() {
  const currentLanguage = languages.find(
    (language) => language.code === defaultLanguage,
  );

  return (
    <Select defaultValue={defaultLanguage}>
      <SelectTrigger
        className="size-10 cursor-pointer justify-center border-0 bg-transparent p-0 shadow-none hover:bg-[rgba(79,124,255,0.08)] focus:ring-0 [&>svg]:hidden"
        aria-label="Chọn ngôn ngữ"
      >
        <SelectValue className="flex-none">
          {currentLanguage && (
            <Image
              src={currentLanguage.flag}
              alt={currentLanguage.name}
              width={20}
              height={20}
              className="size-5 rounded-sm object-cover"
            />
          )}
        </SelectValue>
      </SelectTrigger>

      <SelectContent
        side="bottom"
        sideOffset={8}
        align="end"
        alignItemWithTrigger={false}
        className="w-48 border-[#2C3A55] bg-[#0D1422] p-1.5 text-[#F4F7FF] shadow-[0_18px_40px_rgba(0,0,0,0.45)]"
      >
        {languages.map((language) => (
          <SelectItem
            key={language.code}
            value={language.code}
            className="group cursor-pointer rounded-md px-3 py-2.5 text-[#B8C2D9] transition-colors hover:bg-[rgba(79,124,255,0.10)] hover:text-[#F4F7FF] data-highlighted:bg-[rgba(79,124,255,0.16)] data-highlighted:text-[#F4F7FF] data-[selected]:bg-[rgba(79,124,255,0.16)] data-[selected]:text-[#F4F7FF]"
          >
            <div className="flex w-full items-center gap-2.5">
              <Image
                src={language.flag}
                alt=""
                width={20}
                height={20}
                className="size-5 rounded-sm object-cover"
              />

              <span>{language.name}</span>
            </div>
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}