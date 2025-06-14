import { Component, forwardRef, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { FormControl, FormGroup, NG_VALUE_ACCESSOR, ReactiveFormsModule, Validators } from '@angular/forms';
import { injectContext } from '@taiga-ui/polymorpheus';
import { TuiButton, TuiDialogContext } from '@taiga-ui/core';
import { ClientCreate } from '../../../../state/client/client.model';
import { DialogOptionsWithData } from '../../../../models/dialog-options.model';
import { TuiCalendarMonth, TuiSegmented } from '@taiga-ui/kit';
import { CommonModule } from '@angular/common';
import { TuiInputDateModule, TuiInputModule } from '@taiga-ui/legacy';
import { SelectSexComponent } from './select-sex/select-sex.component';
import { TuiDay } from '@taiga-ui/cdk';
import { DatePickerComponent } from './datepicker/datepicker.component';

function getFormattedDate(dateObj: Date) {
    const year = dateObj.getUTCFullYear();
    const month = String(dateObj.getUTCMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getUTCDate()).padStart(2, '0');
    const hours = String(dateObj.getUTCHours()).padStart(2, '0');
    const minutes = String(dateObj.getUTCMinutes()).padStart(2, '0');
    const seconds = String(dateObj.getUTCSeconds()).padStart(2, '0');
    const microseconds = '000311'; // Фиксированные микросекунды

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${microseconds}+00:00`;
}

@Component({
    selector: 'app-client-form',
    standalone: true,
    templateUrl: 'client-form.component.html',
    styleUrl: 'client-form.component.scss',
    imports: [
        CommonModule,
        ReactiveFormsModule,
        TuiButton,
        TuiInputModule,
        TuiInputDateModule,
        TuiSegmented,
        SelectSexComponent,
        TuiCalendarMonth,
        DatePickerComponent,
    ],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => ClientFormComponent),
            multi: true,
        },
    ],
})
export class ClientFormComponent implements OnInit, OnChanges {
    readonly sexOptions = [
        { value: true, label: 'Мужской' },
        { value: false, label: 'Женский' },
    ] as const;

    readonly violatorOptions = [
        { value: false, label: 'Допущен' },
        { value: true, label: 'Не допущен' },
    ];

    currentDate = [new Date().getDate(), new Date().getMonth(), new Date().getFullYear()];

    public readonly context =
        injectContext<TuiDialogContext<ClientCreate | null, DialogOptionsWithData<ClientCreate | null>>>();

    form = new FormGroup({
        name: new FormControl('', {
            validators: Validators.required,
            nonNullable: true,
        }),
        surname: new FormControl('', {
            validators: Validators.required,
            nonNullable: true,
        }),
        patronymic: new FormControl('', {
            validators: Validators.required,
            nonNullable: true,
        }),
        sex: new FormControl<boolean>(true, {
            validators: Validators.required,
            nonNullable: true,
        }),
        email: new FormControl(''),
        phone: new FormControl('', {
            validators: Validators.required,
            nonNullable: true,
        }),
        photo_url: new FormControl('', {
            validators: Validators.required,
            nonNullable: true,
        }),
        relationships: new FormControl([], {
            nonNullable: true,
        }),
        season_ticket: new FormGroup({
            type: new FormControl('', {
                nonNullable: true,
                validators: Validators.required,
            }),
            expires_at: new FormControl('', {
                nonNullable: true,
            }),
        }),
        comments: new FormControl([], {
            nonNullable: true,
        }),
        is_violator: new FormControl(false, {
            nonNullable: true,
        }),
        last_visit: new FormControl<number>(0, {
            nonNullable: true,
        }),
        last_visit_day: new FormControl<TuiDay | null>(
            new TuiDay(Number(this.currentDate[2]), Number(this.currentDate[1]), Number(this.currentDate[0])),
            {
                nonNullable: true,
            },
        ),
    });

    get last_visit_day(): TuiDay | null {
        const date = new Date();
        return this.form.value.last_visit !== -1
            ? this.context.data
                ? this.getTuiDayWithDifference(this.form.value.last_visit!)
                : new TuiDay(date.getFullYear(), date.getMonth(), date.getDate())
            : null;
    }

    get image(): string {
        return this.form.value.photo_url || '';
    }

    constructor() {}

    ngOnInit(): void {
        let isSyncing = false;

        this.form.controls.last_visit_day.valueChanges.subscribe((value) => {
            if (value === null) {
                this.form.controls.last_visit.setValue(-1, { emitEvent: false });
            } else if (value instanceof TuiDay && !isSyncing) {
                isSyncing = true;
                let creationDate = new Date();

                if (this.context.data && this.context.data.data?.last_visit) {
                    creationDate = new Date(this.context.data.data?.last_visit);
                }

                const selectedDate = new Date(value.year, value.month, value.day);
                const daysDifference =
                    Math.floor((selectedDate.getTime() - creationDate.getTime()) / (1000 * 60 * 60 * 24)) + 1;

                this.form.controls.last_visit.setValue(daysDifference ? daysDifference : 1, {
                    emitEvent: false,
                });
                isSyncing = false;
            }
        });

        this.form.controls.last_visit.valueChanges.subscribe((value) => {
            if (value == -1 || value == null) {
                this.form.controls.last_visit_day.setValue(null, { emitEvent: false });
            } else if (typeof value === 'number' && !isSyncing) {
                isSyncing = true;
                const targetTuiDay = this.getTuiDayWithDifference(value);
                this.form.controls.last_visit_day.setValue(targetTuiDay, { emitEvent: false });
                isSyncing = false;
            }
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        // console.log(changes);
    }

    getTuiDayWithDifference(value: number): TuiDay {
        const creationTimestamp = this.context.data.data?.last_visit ?? new Date().getTime();
        const creationDate = new Date(creationTimestamp);
        const targetDate = new Date(creationDate);
        targetDate.setDate(creationDate.getDate() + value);
        return new TuiDay(targetDate.getFullYear(), targetDate.getMonth(), targetDate.getDate());
    }

    save() {
        console.log(this.form.value);
        const form = this.form.value;

        const randomDays = Math.floor(Math.random() * 359) + 7; // 7-365 дней
        const futureDate = new Date();
        futureDate.setDate(futureDate.getDate() + randomDays);
        form.season_ticket!.expires_at = getFormattedDate(futureDate);

        if (form.email === '') form.email = null;

        if (this.form.valid) {
            this.context.completeWith(form as ClientCreate);
        }
    }

    cancel() {
        this.context.completeWith(null);
    }
}
