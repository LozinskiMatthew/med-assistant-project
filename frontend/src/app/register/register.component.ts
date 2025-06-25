import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  email = '';
  password = '';
  error = '';
  backendErrors = {
    email: '',
    password: ''
  };

  constructor(private auth: AuthService, private router: Router) {}

  register() {
    this.backendErrors = { email: '', password: '' };
    this.error = '';

    this.auth.register(this.email, this.password).subscribe({
      next: () => this.router.navigate(['/login']),
      error: (err) => {
        const errors = err.error;
        this.backendErrors.email = errors?.email?.[0] || '';
        this.backendErrors.password = errors?.password?.[0] || '';

        if (!this.backendErrors.email && !this.backendErrors.password) {
          this.error = 'Registration failed.';
        }
      }
    });
  }
}
