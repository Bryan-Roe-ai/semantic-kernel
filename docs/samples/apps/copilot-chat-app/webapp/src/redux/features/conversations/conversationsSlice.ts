// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

export class DevSkimFixer implements vscode.CodeActionProvider {
    fixMapping = new Map<string, Map<number, CodeFixMapping[]>>();
    public static readonly providedCodeActionKinds = [
        vscode.CodeActionKind.QuickFix
    ];

    createMapKeyForDiagnostic(diagnostic: vscode.Diagnostic, fileName: string): string {
        return `${fileName}: ${diagnostic.message}, ${String(diagnostic.code)}, ${diagnostic.range.start.line}, ${diagnostic.range.start.character}, ${diagnostic.range.end.line}, ${diagnostic.range.end.character}`;
    }

    removeFindingsForOtherVersions(fileVersion: FileVersion) {
        const fileMapping = this.fixMapping.get(fileVersion.fileName);
        if (!fileMapping) {
            return;
        }
        // Additional logic to remove findings for other versions
    }
}



