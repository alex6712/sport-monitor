import { Component } from '@angular/core';
import { LoginComponent } from './login/login.component';
import { ClientbaseComponent } from './clientbase/clientbase.component';
import { MonitoringComponent } from './monitoring/monitoring.component';
import { RegisterComponent } from './register/register.component';

@Component({
    selector: 'app-modules',
    standalone: true,
    imports: [
        LoginComponent,
        ClientbaseComponent,
        MonitoringComponent,
        RegisterComponent,
    ],
    template: '',
})
export class ModulesComponent {}
