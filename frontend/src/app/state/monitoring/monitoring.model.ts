import { Color } from '@swimlane/ngx-charts';

export interface MonitoringData {
    id: string;
    name: string;
    current: number;
    max: number;
}

export interface ChartData {
    id: string;
    title: string;
    chartType?: 'occupancy' | 'demographic' | 'custom';
    timestamp?: Date;
}

export interface CalculatedChartData extends ChartData {
    current: number;
    max: number;
    categoryNames: [string, string];
    statLabels: [string, string];
    colorScheme?: Color;
}

export interface CustomChartData extends ChartData {
    data: ChartDataItem[];
    arcWidth?: number;
}

export interface ChartDataItem {
    name: string;
    value: number;
    color?: string;
}

export type ResponseChartData = CalculatedChartData | CustomChartData;
