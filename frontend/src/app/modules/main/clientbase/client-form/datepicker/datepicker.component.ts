import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, forwardRef, Input, OnDestroy, OnInit } from '@angular/core';
import { ControlValueAccessor, FormControl, NG_VALUE_ACCESSOR, ReactiveFormsModule } from '@angular/forms';
import { TuiDay } from '@taiga-ui/cdk';
import { TuiInputDateModule } from '@taiga-ui/legacy';
import { Subject, takeUntil } from 'rxjs';

type ChangeFunc = (_: TuiDay | unknown | null) => void;

export function getCurrentDate(date: number = 0): TuiDay {
    // TODO: попробовать добавить библу на дату
    const currentDate = date
        ? [new Date(date).getDate(), new Date(date).getMonth(), new Date(date).getFullYear()]
        : [new Date().getDate(), new Date().getMonth(), new Date().getFullYear()];
    return new TuiDay(Number(currentDate[2]), Number(currentDate[1]), Number(currentDate[0]));
}

@Component({
    selector: 'app-date-picker',
    standalone: true,
    imports: [TuiInputDateModule, ReactiveFormsModule, CommonModule],
    templateUrl: './datepicker.component.html',
    styleUrls: ['./datepicker.component.scss'],
    changeDetection: ChangeDetectionStrategy.OnPush,
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => DatePickerComponent),
            multi: true,
        },
    ],
})
export class DatePickerComponent implements ControlValueAccessor, OnInit, OnDestroy {
    @Input()
    settedTime!: TuiDay | null;

    currentDate = [new Date().getDate(), new Date().getMonth(), new Date().getFullYear()];
    unlimitControl = new FormControl<boolean>(false); // Контрол для переключателя "Бессрочно"
    dateControl = new FormControl<TuiDay | null>(null); // Контрол для выбранной даты
    readonly minDate = getCurrentDate();

    private destroy$ = new Subject<void>(); // Используется для отписки от Observable
    onChange: ChangeFunc = () => {}; // используется для библиотеки, не удалять

    setCurrentTuiDate(currentDate: TuiDay | null): void {
        this.dateControl.setValue(currentDate);
        this.onDateChange(currentDate);
    }

    ngOnInit() {
        this.setCurrentTuiDate(this.settedTime);

        this.unlimitControl.valueChanges.pipe(takeUntil(this.destroy$)).subscribe((unlimited) => {
            if (unlimited) {
                this.setCurrentTuiDate(null);
            } else {
                if (!this.dateControl.value || !this.settedTime) {
                    const newCurrentDate = new TuiDay(
                        Number(this.currentDate[2]),
                        Number(this.currentDate[1]),
                        Number(this.currentDate[0]),
                    );
                    this.setCurrentTuiDate(newCurrentDate);
                } else {
                    this.setCurrentTuiDate(this.settedTime);
                }
            }
            this.dateControl.enable();
        });

        // Слушаем изменения в контроле даты
        this.dateControl.valueChanges.pipe(takeUntil(this.destroy$)).subscribe((date) => {
            if (!this.unlimitControl.value) {
                this.onDateChange(date);
            }
        });
    }

    // Метод, используемый Angular Forms для установки значения компонента
    // Необходима реализация при наследовании ControlValueAccessor
    writeValue(date: TuiDay | null) {
        if (date instanceof TuiDay || date === null) {
            this.dateControl.setValue(date);
            this.unlimitControl.setValue(!date);
        } else {
            this.dateControl.setValue(null);
        }
    }

    // Регистрация функции изменения значения для Angular Forms
    // Необходима реализация при наследовании ControlValueAccessor
    registerOnChange(fn: ChangeFunc) {
        this.onChange = fn;
        this.setCurrentTuiDate(this.settedTime);
    }

    // не удалять, нужна для регистрации нажатий для Angular Forms
    // Необходима реализация при наследовании ControlValueAccessor
    registerOnTouched(fn: any) {}

    onDateChange(date: unknown) {
        if (!this.unlimitControl.value) {
            this.onChange(date);
        } else {
            this.onChange(null);
        }
    }

    ngOnDestroy() {
        this.destroy$.next();
        this.destroy$.complete();
    }
}
