import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
// 1. IMPORTAR ENVIRONMENT
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class unirseHogarService {
  // 2. USAR URL DEL ENTORNO
  private apiUrl = environment.apiUrl + 'bienvenida';

  constructor(private http: HttpClient) {}

  unirseHogar(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return this.http.post<any>(this.apiUrl, data, { headers });
  }
}
