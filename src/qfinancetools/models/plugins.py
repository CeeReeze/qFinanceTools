from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PluginCapability(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    description: str


class PluginMeta(BaseModel):
    model_config = ConfigDict(frozen=True)

    plugin_id: str
    name: str
    version: str
    capabilities: list[PluginCapability] = Field(default_factory=list)
    error: str | None = None


class PluginRegistrySnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    plugins: list[PluginMeta] = Field(default_factory=list)
