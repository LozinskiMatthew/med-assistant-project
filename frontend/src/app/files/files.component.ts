import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-files',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './files.component.html',
  styleUrls: ['./files.component.css']
})
export class FilesComponent {
  files: any[] = [];
  selectedFile: File | null = null;
  title: string = '';

  constructor(private http: HttpClient, private router: Router) {
    this.loadFiles();
  }

  loadFiles() {
    this.http.get<any[]>('/api/documents/').subscribe(data => {
      this.files = data;
    });
  }

onFileSelected(event: any) {
  const fileInput = event.target as HTMLInputElement;
  const file = fileInput.files?.[0] || null;

  if (file && file.type !== 'application/pdf') {
    alert('Only PDF files are allowed!');
    this.selectedFile = null;
    fileInput.value = '';
    return;
  }

  this.selectedFile = file;
}


  uploadFile() {
    if (this.selectedFile && this.title) {
      const formData = new FormData();
      formData.append('title', this.title);
      formData.append('document_file', this.selectedFile);

      this.http.post('/api/documents/', formData).subscribe(() => {
        this.loadFiles();
        this.selectedFile = null;
        this.title = '';
      });
    } else {
      alert('Please select a file and enter a title.');
    }
  }

    goBack() {
    this.router.navigate(['/dashboard']);
  }

}
