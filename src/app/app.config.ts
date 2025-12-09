// import {
//   ApplicationConfig,
//   provideZonelessChangeDetection,
// } from '@angular/core';
// import { provideRouter, withComponentInputBinding } from '@angular/router';

// import { routes } from './app.routes';
// import {
//   provideClientHydration,
//   withEventReplay,
// } from '@angular/platform-browser';
// import { provideHttpClient, withFetch } from '@angular/common/http';

// export const appConfig: ApplicationConfig = {
//   providers: [
//     provideZonelessChangeDetection(), // ¡Correcto!
//     provideRouter(routes, withComponentInputBinding()),
//     provideHttpClient(withFetch()),
//     provideClientHydration(withEventReplay()),
//   ],
// };

import {
  ApplicationConfig,
  provideZonelessChangeDetection,
} from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZonelessChangeDetection(),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withFetch()),
  ],
};
