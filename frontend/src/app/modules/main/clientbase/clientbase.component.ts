import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Client } from '../../../state/client/client.model';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CREATE_DIALOG_OPTION } from './clientbase.constant';
import { tuiDialog } from '@taiga-ui/core';
import { ClientFormComponent } from './client-form/client-form.component';
import { ClientService } from '../../../state/client/client.service';
import { switchMap, take, tap } from 'rxjs';

@Component({
    selector: 'app-clientbase',
    standalone: true,
    imports: [CommonModule, RouterLink],
    templateUrl: './clientbase.component.html',
    styleUrl: './clientbase.component.scss',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ClientbaseComponent implements OnInit {
    clients: Client[] = [];

    get isClients() {
        return !!this.clients.length;
    }

    readonly createDialogOptions = CREATE_DIALOG_OPTION;

    private readonly dialog = tuiDialog(ClientFormComponent, this.createDialogOptions);

    constructor(private clientService: ClientService, private cdr: ChangeDetectorRef) {}

    ngOnInit(): void {
        this.clientService
            .getClients()
            .pipe(
                take(1),
                tap((data) => {
                    this.clients = data.clients || [];
                    this.cdr.markForCheck();
                }),
            )
            .subscribe();
    }

    showDialog(): void {
        this.dialog(this.createDialogOptions)
            .pipe(
                switchMap((data) => {
                    return this.clientService.createClient(data!);
                }),
                tap((data) => {
                    this.clients = data.clients || [];
                    this.cdr.markForCheck();
                }),
            )
            .subscribe({
                next: (data) => {
                    console.info(`Dialog emitted data = ${data}`);
                },
                complete: () => {
                    console.info('Dialog closed');
                },
            });
    }
}
