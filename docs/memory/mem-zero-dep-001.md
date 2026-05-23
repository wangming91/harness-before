# Memory: 假设 README 中的 pip 安装方式对非 Python 用户足够友好

## Metadata

- ID: mem-zero-dep-001
- Type: false_assumption
- Status: active
- Created: 2026-05-23T03:12:40.535158+00:00
- Updated: 2026-05-23T03:12:40.535439+00:00
- Related: 

## Summary

假设 README 中的 pip 安装方式对非 Python 用户足够友好

## Context

项目要求 Python 3.13+，但很多 AI 协作开发者不熟悉 Python 环境管理，pip editable install 对新手有门槛

## Evidence

- README.md
- pyproject.toml

## Implication

零依赖工具链（uv/uvx）应作为 CLI 项目的首选安装方式，与传统 pip 并列提供

## Deprecation Policy

Mark deprecated when evidence no longer applies.
