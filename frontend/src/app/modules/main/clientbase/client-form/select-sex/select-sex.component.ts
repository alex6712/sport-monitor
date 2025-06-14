import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR, ReactiveFormsModule } from '@angular/forms';
import { TuiSegmented } from '@taiga-ui/kit';
import { TuiButton } from '@taiga-ui/core';

interface SexOption {
    value: boolean;
    label: string;
}

@Component({
    selector: 'app-select-sex',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, TuiSegmented, TuiButton],
    template: `
        <tui-segmented size="m">
            <button
                *ngFor="let opt of options"
                tuiSegmentedItem
                [value]="opt.value"
                [disabled]="isDisabled"
                (click)="setValue(opt.value)"
            >
                {{ opt.label }}
            </button>
        </tui-segmented>
    `,
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: forwardRef(() => SelectSexComponent),
            multi: true,
        },
    ],
    styles: `
        :host {
            width: 100%;
            max-width: 300px;
            min-width: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        tui-segmented {
            width: fit-content;
        }
    `,
})
export class SelectSexComponent implements ControlValueAccessor {
    @Input() options: readonly SexOption[] = [];

    value: boolean | null = null;
    isDisabled = false;

    private onChange: (v: boolean) => void = () => {};
    private onTouched: () => void = () => {};

    writeValue(v: boolean): void {
        this.value = v;
    }

    registerOnChange(fn: (v: boolean) => void): void {
        this.onChange = fn;
    }

    registerOnTouched(fn: () => void): void {
        this.onTouched = fn;
    }

    setDisabledState(disabled: boolean): void {
        this.isDisabled = disabled;
    }

    /** Вызываем при клике */
    setValue(v: boolean) {
        if (this.isDisabled) return;
        this.value = v;
        this.onChange(v);
        this.onTouched();
    }
}
