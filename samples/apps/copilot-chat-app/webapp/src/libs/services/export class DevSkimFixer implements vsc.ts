export class DevSkimFixer implements vscode.CodeActionProvider {
    fixMapping = new Map<string, Map<number, CodeFixMapping[]>>();
    public static readonly providedCodeActionKinds = [
        vscode.CodeActionKind.QuickFix
    ];

    createMapKeyForDiagnostic(diagnostic: vscode.Diagnostic, fileName: string): string {
        return `${fileName}: ${diagnostic.message}, ${String(diagnostic.code)}, ${diagnostic.range.start.line}, ${diagnostic.range.start.character}, ${diagnostic.range.end.line}, ${diagnostic.range.end.character}`;
    }

    removeFindingsForOtherVersions(fileVersion: FileVersion) {
        var keyNames = this.fixMapping.get(fileVersion.fileName)?.keys() ?? new Array<number>();
        for (let key of keyNames) {
            if (key != fileVersion.version) {
                this.fixMapping.get(fileVersion.fileName)?.delete(key);
            }
        }
    }

    ensureMapHasMappings(mapping: CodeFixMapping) {
        if (!this.fixMapping.has(mapping.fileName)) {
            this.fixMapping.set(mapping.fileName, new Map<number, CodeFixMapping[]>());
        }
        if (!this.fixMapping.get(mapping.fileName)?.has(mapping.version)) {
            this.fixMapping.get(mapping.fileName)?.set(mapping.version, []);
        }
        this.fixMapping.get(mapping.fileName)?.get(mapping.version)?.push(mapping);
    }

    provideCodeActions(document: vscode.TextDocument, range: vscode.Range | vscode.Selection, context: vscode.CodeActionContext, token: vscode.CancellationToken): vscode.CodeAction[] {
        const output: vscode.CodeAction[] = [];
        context.diagnostics.filter(diagnostic => String(diagnostic.source).startsWith("DevSkim Language Server")).forEach((filteredDiagnostic: vscode.Diagnostic) => {
            const diagnosticKey = this.createMapKeyForDiagnostic(filteredDiagnostic, document.uri.toString().replace(/%3A/g, ":"));
            this.fixMapping.get(document.uri.toString().replace(/%3A/g, ":"))?.get(document.version)?.forEach(codeFix => {
                if (diagnosticKey == this.createMapKeyForDiagnostic(codeFix.diagnostic, codeFix.fileName)) {
                    output.push(this.createFix(document, filteredDiagnostic, codeFix));
                }
            });
        });
        return output;
    }

    private createFix(document: vscode.TextDocument, diagnostic: vscode.Diagnostic, codeFix: CodeFixMapping): vscode.CodeAction {
        const fix = new vscode.CodeAction(codeFix.friendlyString, vscode.CodeActionKind.QuickFix);
        fix.edit = new vscode.WorkspaceEdit();
        if (!codeFix.isSuppression) {
            fix.edit.replace(document.uri, diagnostic.range, codeFix.replacement);
        } else {
            const line = document.lineAt(diagnostic.range.end.line);
            fix.edit.insert(document.uri, line.range.end, codeFix.replacement);
        }
        return fix;
    }
}
