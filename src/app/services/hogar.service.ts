import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { BehaviorSubject } from 'rxjs';
import { RespuestaHogar } from '../bienvenida/bienvenida.interface';

import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class HogarService {
  private apiUrl = environment.apiUrl + 'bienvenida';
  private apiconsultarhogar = environment.apiUrl + 'consultarHogar';
  private apisalirHogar = environment.apiUrl + 'salirHogar';

  private apiresidentes = environment.apiUrl.replace(/\/$/, '');
  private apicategoriashogar = environment.apiUrl + 'categorias-hogar/agregar';
  private apicategoriasdisponibles =
    environment.apiUrl + 'categorias/disponible/';

  constructor(private http: HttpClient) {}

  crearHogar(datos: any) {
    return this.http.post(`${this.apiUrl}`, datos);
  }

  obtenerHogarActual(token: string): Observable<RespuestaHogar> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = { token: token };

    return this.http.post<RespuestaHogar>(this.apiconsultarhogar, body, {
      headers,
    });
  }

  salirseDelHogar(token: string) {
    return this.http.post(`${this.apisalirHogar}`, {
      token: `Bearer ${token}`,
    });
  }

  agregarCategoriaAHogar(datos: any): Observable<any> {
    return this.http.post(this.apicategoriashogar, datos);
  }

  obtenerCategoriasDisponibles(idHogar: number): Observable<any> {
    return this.http.get(`${this.apicategoriasdisponibles}${idHogar}`);
  }

  obtenerCategoriasSeleccionadas(idHogar: number): Observable<any[]> {
    return this.http.get<any[]>(
      `${environment.apiUrl}categorias/seleccionadas/${idHogar}`
    );
  }

  getResidentes(idHogar: number) {
    return this.http.get<{ status: string; residentes: any[] }>(
      `${this.apiresidentes}/hogar/residentes/${idHogar}`
    );
  }

  crearTicket(ticket: any): Observable<any> {
    return this.http.post(`${this.apiresidentes}/tickets`, ticket);
  }

  obtenerTicketsPendientes(idHogar: number): Observable<any> {
    return this.http.get<any>(
      `${this.apiresidentes}/tickets/pendientes/${idHogar}`
    );
  }

  actualizarEstadoTicket(idTicket: number, estado: string): Observable<any> {
    return this.http.put<any>(
      `${this.apiresidentes}/tickets/${idTicket}/estado`,
      { estado }
    );
  }

  private nombreHogarSubject = new BehaviorSubject<string>('');
  nombreHogar$ = this.nombreHogarSubject.asObservable();

  private idHogarSubject = new BehaviorSubject<number | null>(null);
  idHogar$ = this.idHogarSubject.asObservable();

  private esCreadorSubject = new BehaviorSubject<boolean>(false);
  esCreador$ = this.esCreadorSubject.asObservable();

  private idUsuarioSubject = new BehaviorSubject<number | null>(null);
  idUsuario$ = this.idUsuarioSubject.asObservable();

  setNombreHogar(nombre: string) {
    this.nombreHogarSubject.next(nombre);
  }

  getNombreHogar(): string {
    return this.nombreHogarSubject.value;
  }

  setIdHogar(id: number) {
    this.idHogarSubject.next(id);
  }

  getIdHogar(): number | null {
    return this.idHogarSubject.value;
  }

  setEsCreador(esCreador: boolean) {
    this.esCreadorSubject.next(esCreador);
  }

  getEsCreador(): boolean {
    return this.esCreadorSubject.value;
  }

  setIdUsuario(id_usuario: number) {
    this.idUsuarioSubject.next(id_usuario);
    sessionStorage.setItem('IdUsuario', id_usuario.toString());
  }

  getIdUsuario(): number | null {
    return this.idUsuarioSubject.value;
  }
}
