import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';
  success = '';
  backendErrors = {
    email: '',
    password: ''
  };

  constructor(private auth: AuthService, private router: Router) {}

  login() {
    this.backendErrors = { email: '', password: '' };
    this.error = '';
    this.success = '';

    this.auth.login(this.email, this.password).subscribe({
      next: (res: any) => {
        localStorage.setItem('access', res.access);
        this.success = 'Login successful!';
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        const errors = err.error;

        this.backendErrors.email = errors?.email?.[0] || '';
        this.backendErrors.password = errors?.password?.[0] || '';

        if (!this.backendErrors.email && !this.backendErrors.password) {
          this.error = 'Invalid credentials';
        }
      }
    });
  }
}
