import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import {FormsModule} from "@angular/forms";
import {NgIf} from "@angular/common";
@Component({
  selector: 'app-account',
  standalone: true,
  imports: [
    FormsModule,
    NgIf
  ],
  templateUrl: './account.component.html',
  styleUrl: './account.component.css'
})
export class AccountComponent implements OnInit {
  user: any = {};
  editMode = false;
  newEmail = '';
  newPassword = '';
  newUsername = '';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchProfile();
  }

  get headers() {
    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${localStorage.getItem('access')}`
      })
    };
  }

  fetchProfile() {
    this.http.get<any>('/api/profile/', this.headers).subscribe({
      next: res => {
        this.user = res;
        this.newEmail = res.email || '';
        this.newUsername = res.username || '';
      },
      error: err => {
        console.error(err);
        if (err.status === 401) this.router.navigate(['/login']);
      }
    });
  }

  updateProfile() {
    const data: any = {
      email: this.newEmail
    };
    if (this.newPassword) data.password = this.newPassword;
    if (this.newUsername) data.username = this.newUsername;

    this.http.put('/api/profile/', data, this.headers).subscribe({
      next: () => {
        this.editMode = false;
        this.fetchProfile();
      },
      error: err => console.error(err)
    });
  }

  logout() {
    const refresh = localStorage.getItem('refresh');
    this.http.post('/api/logout/', { refresh }, this.headers).subscribe({
      next: () => {
        localStorage.clear();
        this.router.navigate(['/login']);
      },
      error: err => console.error(err)
    });
  }

  deleteAccount() {
    if (!confirm('Are you sure you want to delete your account?')) return;

    this.http.delete('/api/delete-account/', this.headers).subscribe({
      next: () => {
        localStorage.clear();
        this.router.navigate(['/register']);
      },
      error: err => console.error(err)
    });
  }
}
