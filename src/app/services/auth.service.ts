import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
// 1. IMPORTAR ENVIRONMENT (Asegúrate que la ruta sea correcta)
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  // 2. BORRAMOS LAS VARIABLES FIJAS QUE TENÍAS ANTES
  // private apiUrl = 'http://:5000/login';  <-- ESTO ESTABA MAL
  // private apiregistro = 'http://localhost:5000/registro'; <-- ESTO ERA EL ERROR

  constructor(private http: HttpClient) {}

  login(usuario: string, password: string): Observable<any> {
    const body = { usuario, password };

    // 3. USAMOS LA URL DEL ENTORNO + EL ENDPOINT
    // Si environment.apiUrl es '...onrender.com/', aquí se forma '...onrender.com/login'
    const urlLogin = environment.apiUrl + 'login';

    return new Observable((observer) => {
      this.http.post<any>(urlLogin, body).subscribe({
        next: (response) => {
          if (response && response.status === 'Correcto') {
            const token = response.token;
            const tokenPayload = this.decodeToken(token);

            const usuarioGuardado = {
              id: tokenPayload?.id_usuario || 0,
              nombre: usuario,
            };

            sessionStorage.setItem('token', token);
            sessionStorage.setItem('usuario', JSON.stringify(usuarioGuardado));

            console.log('Token guardado en sessionStorage:', token);
            console.log('Usuario guardado en sessionStorage:', usuarioGuardado);

            observer.next(response);
            observer.complete();
          } else {
            console.error('Respuesta de login inesperada:', response);
            observer.error('Formato de respuesta inválido');
          }
        },
        error: (err) => {
          console.error('Error en login:', err);
          observer.error(err);
        },
      });
    });
  }

  private decodeToken(token: string): any {
    try {
      const payloadBase64 = token.split('.')[1];
      const payload = JSON.parse(atob(payloadBase64));
      return payload;
    } catch (error) {
      console.error('Error decoding token:', error);
      return null;
    }
  }

  obtenerUsuarioActual(): { id: number; nombre: string } | null {
    const usuario = sessionStorage.getItem('usuario');
    return usuario ? JSON.parse(usuario) : null;
  }

  getToken(): string | null {
    return sessionStorage.getItem('token');
  }

  registro(
    usuario: string,
    password: string,
    correo: string,
    telefono: string
  ): Observable<any> {
    const body = { usuario, password, correo, telefono };

    // 4. LO MISMO AQUÍ PARA REGISTRO
    const urlRegistro = environment.apiUrl + 'registro';

    return this.http.post(urlRegistro, body);
  }
}
