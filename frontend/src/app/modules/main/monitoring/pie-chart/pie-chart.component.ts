import { Component, Input, OnChanges } from '@angular/core';
import { Color, NgxChartsModule, ScaleType } from '@swimlane/ngx-charts';
import { CommonModule } from '@angular/common';
import { ChartDataItem } from '../../../../state/monitoring/monitoring.model';

@Component({
    standalone: true,
    imports: [CommonModule, NgxChartsModule],
    selector: 'app-pie-chart',
    templateUrl: './pie-chart.component.html',
    styleUrls: ['./pie-chart.component.scss'],
})
export class PieChartComponent implements OnChanges {
    @Input({ required: true }) title!: string;
    @Input() view: [number, number] = [400, 400];

    @Input() data?: ChartDataItem[];

    @Input() current?: number;
    @Input() max?: number;
    @Input() categoryNames: [string, string] = ['Занято', 'Свободно'];

    @Input() statLabels: [string, string] = ['Занято', 'Свободно'];
    @Input() colorScheme: Color = {
        name: 'customScheme',
        selectable: true,
        group: ScaleType.Linear,
        domain: ['#E44D25', '#5AA454', '#CCFF00', '#CC0066', '#FF6633'],
    };
    @Input() arcWidth: number = 0.15;

    chartData: ChartDataItem[] = [];

    ngOnChanges() {
        this.updateChartData();
    }

    private updateChartData() {
        if (this.data) {
            this.chartData = this.data;
            return;
        }

        if (this.current === undefined || this.max === undefined) return;

        const safeCurrent = Math.min(this.current, this.max);
        this.chartData = [
            {
                name: this.categoryNames[0],
                value: safeCurrent,
            },
            {
                name: this.categoryNames[1],
                value: Math.max(this.max - safeCurrent, 0),
            },
        ];
    }

    get displayStats() {
        if (!this.current || !this.max) return null;

        return {
            current: `${this.statLabels[0]}: ${this.current}`,
            free: `${this.statLabels[1]}: ${this.max - this.current}`,
        };
    }

    get displayData() {
        if (!this.data) return null;

        return this.data;
    }
}
