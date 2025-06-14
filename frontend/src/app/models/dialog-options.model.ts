import { TuiDialogContext } from '@taiga-ui/core';
import { PolymorpheusContent } from '@tinkoff/ng-polymorpheus';

export interface DialogOptionsWithData<T> {
    content: PolymorpheusContent<TuiDialogContext<void, T>>;
    heading: string;
    label: string;
    buttons: string[];
    size: 's' | 'm' | 'l' | 'auto';
    data?: T;
}
