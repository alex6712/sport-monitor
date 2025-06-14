import { Routes } from '@angular/router';
import { LoginComponent } from './modules/login/login.component';
import { ClientbaseComponent } from './modules/main/clientbase/clientbase.component';
import { MonitoringComponent } from './modules/main/monitoring/monitoring.component';
import { AuthGuard } from './core/guards/loged-in.guard';
import { MainComponent } from './modules/main/main.component';

export const routes: Routes = [
    { path: '', redirectTo: 'main/monitoring', pathMatch: 'full' },
    {
        path: 'login',
        title: 'Вход',
        component: LoginComponent,
    },
    {
        path: 'main',
        title: 'Управление',
        canActivate: [AuthGuard],
        component: MainComponent,
        children: [
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
        ],
    },
];
