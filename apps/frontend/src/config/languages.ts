import vietnamFlag from "@/assets/images/vietnam_flag.jpg";

export const languages = [
  {
    code: "vi",
    name: "Tiếng Việt",
    flag: vietnamFlag,
  },
] as const;

export type LanguageCode = (typeof languages)[number]["code"];

export const defaultLanguage: LanguageCode = "vi";