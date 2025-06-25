import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

export const AuthInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access');
  const router = inject(Router);

  const publicUrls = ['/api/login/', '/api/register/'];
  if (publicUrls.some(url => req.url.includes(url))) {
    return next(req);
  }

  const cloned = token
    ? req.clone({ headers: req.headers.set('Authorization', `Bearer ${token}`) })
    : req;

  return next(cloned).pipe(
    catchError(err => {
      if (err.status === 401) {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        router.navigate(['/login']);
      }

      return throwError(() => err);
    })
  );
};
