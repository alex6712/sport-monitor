import { DialogOptionsWithData } from '../../../models/dialog-options.model';

export const CREATE_DIALOG_OPTION: DialogOptionsWithData<null> = {
    data: null,
    heading: 'Новый клиент',
    label: 'Новый клиент',
    buttons: ['Создать', 'Отмена'],
    size: 'auto',
    content: undefined,
};
