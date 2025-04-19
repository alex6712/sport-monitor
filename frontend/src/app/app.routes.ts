import { Routes } from '@angular/router';
import { LoginComponent } from './modules/login/login.component';
import { ClientbaseComponent } from './modules/clientbase/clientbase.component';
import { MonitoringComponent } from './modules/monitoring/monitoring.component';
import { AuthGuard } from './core/guards/loged-in.guard';

export const routes: Routes = [
    { path: '', redirectTo: 'monitoring', pathMatch: 'full' },
    {
        path: 'login',
        title: 'Вход',
        component: LoginComponent,
    },
    {
        path: 'monitoring',
        title: 'Мониторинг',
        canActivate: [AuthGuard],
        component: MonitoringComponent,
    },
    {
        path: 'clientbase',
        title: 'База клиентов',
        canActivate: [AuthGuard],
        component: ClientbaseComponent,
    },
];
