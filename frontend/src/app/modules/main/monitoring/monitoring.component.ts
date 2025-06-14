import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { PieChartComponent } from './pie-chart/pie-chart.component';
import { CommonModule } from '@angular/common';
import { MonitoringService } from '../../../state/monitoring/monitoring.service';
import { CalculatedChartData, CustomChartData } from '../../../state/monitoring/monitoring.model';

@Component({
    selector: 'app-monitoring',
    standalone: true,
    imports: [CommonModule, PieChartComponent],
    templateUrl: './monitoring.component.html',
    styleUrl: './monitoring.component.scss',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class MonitoringComponent implements OnInit {
    private isFirstLoading = true;

    twoPartsData: CalculatedChartData[] = [
        {
            id: 'sex',
            title: 'Пол',
            chartType: 'custom',
            current: 120,
            max: 200,
            categoryNames: ['Мужчины', 'Женщины'],
            statLabels: ['Мужчины', 'Женщины'],
            colorScheme: undefined,
        },
        {
            id: 'main-hall',
            title: 'Главный зал',
            chartType: 'occupancy',
            current: 120,
            max: 200,
            categoryNames: ['Посетители', 'Свободно'],
            statLabels: ['Людей', 'Свободно'],
            colorScheme: undefined,
        },
    ];
    severalPartsData: CustomChartData[] = [
        {
            id: 'age-stats',
            chartType: 'demographic',
            title: 'Возрастные группы',
            data: [
                { name: '0-6', value: 2 },
                { name: '7-17', value: 5 },
                { name: '18-30', value: 45 },
                { name: '31-55', value: 25 },
                { name: '56+', value: 30 },
            ],
        },
        {
            id: 'time-day-stats',
            title: 'Время суток',
            data: [
                { name: 'Утро', value: 10 },
                { name: 'День', value: 30 },
                { name: 'Вечер', value: 45 },
                { name: 'Ночь', value: 15 },
            ],
        },
    ];

    constructor(private monitoringService: MonitoringService, private cdr: ChangeDetectorRef) {}

    ngOnInit() {
        if (this.isFirstLoading) this.initChartsData();
        else this.reloadChartsData();
    }

    initChartsData() {
        // this.monitoringService
        //     .getAllMonitorings()
        //     .pipe(
        //         map((newData) => {
        //             console.log(newData);
        //             this.twoPartsData = newData;
        //             this.cdr.markForCheck();
        //         }),
        //     )
        //     .subscribe();
    }

    reloadChartsData() {
        // this.monitoringService
        //     .getLiveUpdates()
        //     .pipe(
        //         map((newData) => {
        //             console.log(newData);
        //             this.severalPartsData = newData;
        //             this.cdr.markForCheck();
        //         }),
        //     )
        //     .subscribe();
    }
}
