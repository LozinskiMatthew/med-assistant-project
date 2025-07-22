import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { AuthInterceptor } from './app/auth.interceptor';

bootstrapApplication(AppComponent, {
  // keep everything that was in appConfig …
  ...appConfig,

  // …and merge (or start) a providers array that adds HttpClient + interceptor
  providers: [
    ...(appConfig.providers ?? []),      // preserve any existing providers
    provideHttpClient(withInterceptors([AuthInterceptor])),
  ],
}).catch(err => console.error(err));
