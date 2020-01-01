#!/usr/bin/env node

"use strict";

const commandLineArgs = require('command-line-args');
const commandLineUsage = require('command-line-usage');

const INC_INDENTS = [
    'CONSTRUCTOR_ENTRY',
    'DML_BEGIN',
    'EXECUTION_STARTED',
    'METHOD_ENTRY',
    'SYSTEM_METHOD_ENTRY'
];
const DEC_INDENTS = [
    'CONSTRUCTOR_EXIT',
    'DML_END',
    'METHOD_EXIT',
    'SYSTEM_METHOD_EXIT'
];
const RM_INDENTS = [
    'EXECUTION_FINISHED'
];

const optionDefinitions = [
    {
        name: 'encoding',
        alias: 'e',
        defaultValue: 'UTF-8',
        type: String
    },
    {
        name: 'lineEnding',
        alias: 'l',
        defaultValue: '\n',
        type: String
    },
    {
        name: 'help',
        alias: 'h',
        type: Boolean,
        description: 'show help'
    }
];

function readCommands() {
    return commandLineArgs(optionDefinitions);
}

function printUsage() {
    const sections = [
        {
            header: 'Salesforce apex log indention tool.',
            content: 'Add indent charactors to apex debug log.'
        },
        {
            header: 'Options',
            optionList: optionDefinitions
        }
    ];
    const usage = commandLineUsage(sections);
    console.log(usage);
}

const LINE_REGEX = /\d{2}:\d{2}:\d{2}\.\d+ \(\d+\)\|([A-Z_]+).*/;

function calcCurrentIndent(currentIndent, lineStr) {
    let result = lineStr.match(LINE_REGEX);
    if (result) {
        let first = result[1];
        if (INC_INDENTS.indexOf(first) >= 0) {
            return [currentIndent, currentIndent + 1];
        }
        if (DEC_INDENTS.indexOf(first) >= 0) {
            currentIndent = currentIndent > 0 ? currentIndent - 1 : 0;
            return [currentIndent, currentIndent];
        }
        if (RM_INDENTS.indexOf(first) >= 0) {
            return [0, 0];
        }
    }
    return [currentIndent, currentIndent];
}

function toIndent(indent) {
    let str = '';
    for (var i = 0; i < indent; i++) {
        str = str + '    ';
    }
    return str;
}

function readStream(inputText, lineEnding, indentLength) {
    let currentIndention = indentLength;
    inputText.split(lineEnding).forEach(line => {
        let indentions = calcCurrentIndent(currentIndention, line);
        let indent = indentions[0];
        currentIndention = indentions[1];

        process.stdout.write(toIndent(indent) + line + lineEnding);
    });
    return currentIndention;
}

function main() {
    const options = readCommands();
    if(options.help) {
        printUsage();
        process.exit(0);
    }

    const ENCODING = options.encoding;
    const LINE_END = options.lineEnding;

    process.stdin.resume();
    process.stdin.setEncoding(ENCODING);

    let indentLength = 0;
    process.stdin.on('data', str => {
        indentLength = readStream(str, LINE_END, indentLength);
    });
}

main();