import { MappingService } from './../services/mapping.service';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';
import { Observable } from 'rxjs';

@Component({
    selector: 'file-select',
    templateUrl: './file-select.component.html',
    styleUrls: ['./file-select.component.scss'],
    providers: [{
        provide: STEPPER_GLOBAL_OPTIONS, useValue: {showError: true}
    }]
})
export class FileSelectComponent implements OnInit {
    @ViewChild('file_select') file_select;

    public optionalFormGroup: FormGroup;
    public firstFormGroup: FormGroup;
    public secondFormGroup: FormGroup;
    public selected_file: string
    public isOptional = true;
    
    files$: Observable<string[]>;
    
    constructor(private _formBuilder: FormBuilder, private mappingService: MappingService) {}
    
    ngOnInit() {
        this.optionalFormGroup = this._formBuilder.group({
            optionalCtrl: ['']
        });
        this.firstFormGroup = this._formBuilder.group({
            firstCtrl: ['', Validators.required]
        });
    }

    selectionChange($event){
        if($event.selectedStep === this.file_select){
            this.files$ = this.mappingService.getFiles()
        }
    }

    startMapping(){
        if (!this.firstFormGroup.valid){
            return;
        }
        else {
            console.log('Yay!');
            
        }
    }
}
