import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import {DashboardComponent} from "./dashboard/dashboard.component";
import {NotesComponent} from "./notes/notes.component";
import {MedicinesComponent} from "./medicines/medicines.component";
import {AccountComponent} from "./account/account.component";
import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: 'notes', component: NotesComponent, canActivate: [authGuard] },
  { path: 'medicines', component: MedicinesComponent, canActivate: [authGuard] },
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: '**', redirectTo: 'dashboard' },
  { path: 'account', component: AccountComponent, canActivate: [authGuard] },
];
