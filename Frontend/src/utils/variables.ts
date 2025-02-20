import { MarketReportRequest, ReportType } from "../api/models/MarketReport.ts";
import dayjs from "dayjs";
import { CompetitorReportRequest } from "../api/models/CompetitorReport.ts";
import { Option } from "../shared/MultiSelect/MultiSelect.tsx";

export const initialMarketReportRequest: MarketReportRequest = {
  title: "Новый отчет",
  type: ReportType.MARKET,
  market: "",
  marketNiche: "",
  autoupdate: 0,
  splitByDates: false,
  datesOfReview: {
    by: "month",
    from: dayjs(),
    to: dayjs(),
  },
  blocks: [
    {
      id: "1",
      isDefault: true,
      type: "text",
      title: "Определение продуктовой ниши",
      split: false,
      by: "",
      splitByDates: false,
      indicators: ["Драйверы роста", "Ограничения роста", "Тренды в развитии"],
    },
    {
      id: "2",
      isDefault: true,
      type: "table",
      title: "Объемы рынка",
      split: true,
      by: "Ниша",
      splitByDates: false,
      indicators: ["Доли рыночных ниш", "Количество потребителей"],
    },
    {
      id: "3",
      isDefault: true,
      type: "text",
      title: "Распределение по регионам",
      split: true,
      by: "Регион РФ",
      splitByDates: false,
      indicators: ["Доля региона", "Количество потребителей"],
    },
    {
      id: "4",
      isDefault: true,
      type: "table",
      title: "Лидеры рынка",
      split: true,
      by: "Компания",
      splitByDates: true,
      indicators: [
        "Доля на рынке",
        "Доходы",
        "Расходы",
        "EBITDA",
        "Чистая прибыль",
      ],
    },
    {
      id: "5",
      isDefault: true,
      type: "table",
      title: "Лидеры по потреблению",
      split: true,
      by: "Потребитель",
      splitByDates: true,
      indicators: ["Доля"],
    },
    {
      id: "6",
      isDefault: true,
      type: "table",
      title: "Прирост потребителей",
      split: true,
      by: "Ниша",
      splitByDates: true,
      indicators: ["Количество потребителей"],
    },
  ],
};

export const initialCompetitorReportRequest: CompetitorReportRequest = {
  title: "Новый отчет",
  type: ReportType.COMPETITOR,
  competitorName: "",
  autoupdate: 0,
};

export const autoupdateOptions: Option[] = [
  {
    label: "Каждый день",
    value: "1",
  },
  {
    label: "Каждую неделю",
    value: "2",
  },
  {
    label: "Каждый месяц",
    value: "3",
  },
  {
    label: "Каждый год",
    value: "4",
  },
];

export const thematics = [
  {
    id: "1",
    value: "Металлургия",
    niches: ["Черная металлургия", "Цветная металлургия"],
  },
  {
    id: "2",
    value: "Добыча полезных ископаемых",
    niches: ["Нефть", "Уголь"],
  },
];

export function isJsonObject(strData: string) {
  try {
    JSON.parse(strData);
  } catch (e) {
    return false;
  }
  return true;
}
