import { Injectable } from '@angular/core';
import { TuiDialogService } from '@taiga-ui/core';
import { ClientFormComponent } from './client-form.component';
import { PolymorpheusComponent } from '@tinkoff/ng-polymorpheus';
import { Client, ClientCreate } from '../../../../state/client/client.model';
import { DialogOptionsWithData } from '../../../../models/dialog-options.model';

@Injectable({
    providedIn: 'root',
})
export class CleintFormService {
    private readonly clientForm = new PolymorpheusComponent(
        ClientFormComponent,
    );

    constructor(private readonly dialogs: TuiDialogService) {}

    openClientForm(options: DialogOptionsWithData<Client | null>) {
        return this.dialogs.open<ClientCreate | null>(this.clientForm, options);
    }
}
