# ganger

Generic job runner handling dependencies.

## Introduction

The main idea is to provide a directed graph of jobs, where the edges mark job dependencies, along with a job runner that can run your jobs. Ganger will then ensure the jobs get completed.