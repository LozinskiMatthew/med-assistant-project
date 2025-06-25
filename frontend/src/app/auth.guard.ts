import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = () => {
  const token = localStorage.getItem('access');
  const router = inject(Router);

  if (!token) {
    router.navigate(['/login']);
    return false;
  }

  return true;
};
