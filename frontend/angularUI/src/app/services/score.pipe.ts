import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'confidenceScore'})
export class ConfidenceScorePipe implements PipeTransform {
    transform(value: number): string{
        if (value >= 80){
            return 'High confidence';
        }
        else if (value < 80 && value >= 30){
            return 'Medium confidence';
        }
        return 'Low confidence';
    }
}