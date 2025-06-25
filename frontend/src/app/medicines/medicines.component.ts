import { Component, OnInit } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { CommonModule, NgIf, NgForOf } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-medicines',
  standalone: true,
  imports: [CommonModule, FormsModule, NgIf, NgForOf, RouterLink],
  templateUrl: './medicines.component.html',
  styleUrls: ['./medicines.component.css']
})
export class MedicinesComponent implements OnInit {
  medicines: any[] = [];
  newMedicine = {
    title: '',
    description: '',
    dosage: '',
    date: ''
  };
  editingMedicineId: number | null = null;

  errors = {
    title: '',
    description: '',
    dosage: '',
    date: ''
  };

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadMedicines();
  }

  loadMedicines() {
    this.http.get<any[]>('/api/profile/medicines/').subscribe((data) => {
      this.medicines = data.sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
      );
    });
  }

  addMedicine() {
    this.errors = { title: '', description: '', dosage: '', date: '' };

    if (!this.newMedicine.title.trim()) this.errors.title = 'Title is required.';
    if (!this.newMedicine.description.trim()) this.errors.description = 'Description is required.';
    if (!this.newMedicine.dosage.trim()) this.errors.dosage = 'Dosage is required.';
    if (!this.newMedicine.date.trim()) this.errors.date = 'Date and time are required.';

    if (Object.values(this.errors).some(val => val)) return;

    const payload = {
      ...this.newMedicine,
      date: new Date(this.newMedicine.date).toISOString()
    };

    if (this.editingMedicineId === null) {
      this.http.post('/api/profile/medicines/', payload).subscribe(() => {
        this.resetForm();
        this.loadMedicines();
      });
    } else {
      this.http.put(`/api/profile/medicines/${this.editingMedicineId}/`, payload).subscribe(() => {
        this.resetForm();
        this.loadMedicines();
      });
    }
  }

  deleteMedicine(id: number) {
    this.http.delete(`/api/profile/medicines/${id}/`).subscribe(() => {
      this.loadMedicines();
    });
  }

  startEdit(medicine: any) {
    this.editingMedicineId = medicine.id;
    this.newMedicine = {
      title: medicine.title,
      description: medicine.description,
      dosage: medicine.dosage,
      date: medicine.date?.slice(0, 16) || ''
    };
    this.errors = { title: '', description: '', dosage: '', date: '' };
  }

  cancelEdit() {
    this.resetForm();
  }

  private resetForm() {
    this.newMedicine = { title: '', description: '', dosage: '', date: '' };
    this.errors = { title: '', description: '', dosage: '', date: '' };
    this.editingMedicineId = null;
  }
}

