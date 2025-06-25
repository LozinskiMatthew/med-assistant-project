import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-notes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './notes.component.html',
  styleUrl: './notes.component.css'
})
export class NotesComponent implements OnInit {
  notes: any[] = [];
  newNote = { title: '', text: '' };
  editingNoteId: number | null = null;

  errors = {
    title: '',
    text: ''
  };

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadNotes();
  }

  loadNotes() {
    this.http.get('/api/profile/notes/').subscribe((data: any) => {
      this.notes = data;
    });
  }

  addNote() {
    this.errors = { title: '', text: '' };

    if (!this.newNote.title.trim()) {
      this.errors.title = 'Title is required.';
    }
    if (!this.newNote.text.trim()) {
      this.errors.text = 'Text is required.';
    }

    if (this.errors.title || this.errors.text) return;

    this.http.post('/api/profile/notes/', this.newNote).subscribe(() => {
      this.newNote = { title: '', text: '' };
      this.loadNotes();
    });
  }

  deleteNote(id: number) {
    this.http.delete(`/api/profile/notes/${id}/`).subscribe(() => {
      this.loadNotes();
    });
  }

  startEdit(note: any) {
    this.editingNoteId = note.id;
    this.newNote = { title: note.title, text: note.text };
    this.errors = { title: '', text: '' };
  }

  updateNote() {
    if (this.editingNoteId === null) return;

    if (!this.newNote.title.trim()) {
      this.errors.title = 'Title is required.';
    }
    if (!this.newNote.text.trim()) {
      this.errors.text = 'Text is required.';
    }

    if (this.errors.title || this.errors.text) return;

    this.http.put(`/api/profile/notes/${this.editingNoteId}/`, this.newNote).subscribe(() => {
      this.editingNoteId = null;
      this.newNote = { title: '', text: '' };
      this.loadNotes();
    });
  }

  cancelEdit() {
    this.editingNoteId = null;
    this.newNote = { title: '', text: '' };
    this.errors = { title: '', text: '' };
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }
}
