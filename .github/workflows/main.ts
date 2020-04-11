
import * as core from '@actions/core';
import * as github from '@actions/github';
const client: github.GitHub = new github.GitHub(
      core.getInput('repo-token', {required: true})
    );
if (isIssue) {
      await client.issues.createComment({
        owner: issue.owner,
        repo: issue.repo,
        issue_number: issue.number,
        body: message
      });
      
