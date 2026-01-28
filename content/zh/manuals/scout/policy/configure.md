---
title: 配置策略
description: 了解如何在 Docker Scout 中配置、禁用或删除策略
keywords: scout, policy, configure, delete, enable, parametrize, thresholds
---

某些策略类型是可配置的。这意味着您可以使用自己的配置参数创建该策略类型的新的自定义版本。如果需要暂时忽略某个策略，您也可以禁用它，或者如果某个策略不符合您的需求，可以完全删除它。

> [!NOTE]
> 如果您删除或自定义策略，默认策略配置的历史评估结果将被移除。

## 添加策略

要添加新策略，请选择您要自定义的策略类型。所有自定义策略都使用策略类型作为基础。

您可以编辑新策略的显示名称和描述，以帮助更好地传达策略的合规和不合规状态。您不能更改策略类型的名称，只能更改其显示名称。

策略的可用配置参数取决于您正在编辑的策略类型。有关更多信息，请参阅[策略类型](/manuals/scout/policy/_index.md#policy-types)。

添加策略的步骤：

1. 前往 Docker Scout 仪表板中的[策略页面](https://scout.docker.com/reports/policy)。
2. 选择 **Add policy** 按钮以打开策略配置屏幕。
3. 在策略配置屏幕上，找到您要配置的策略类型，然后选择 **Configure** 以打开策略配置页面。

   - 如果 **Configure** 按钮显示为灰色，表示当前策略没有可配置的参数。
   - 如果按钮显示为 **Integrate**，表示在启用策略之前需要进行设置。选择 **Integrate** 将引导您查看集成设置指南。

4. 更新策略参数。
5. 保存更改：

   - 选择 **Save policy** 以提交更改并为当前组织启用策略。
   - 选择 **Save and disable** 以保存策略配置但不启用它。

## 编辑策略

编辑策略可让您修改其配置，而无需从头开始创建新策略。当由于需求变化或组织合规目标发生变更而需要调整策略参数时，这非常有用。

编辑策略的步骤：

1. 前往 Docker Scout 仪表板中的[策略页面](https://scout.docker.com/reports/policy)。
2. 选择您要编辑的策略。
3. 选择 **Edit** 按钮。
4. 更新策略参数。
5. 保存更改。

## 禁用策略

当您禁用策略时，该策略的评估结果将被隐藏，不再出现在 Docker Scout 仪表板或 CLI 中。如果您禁用策略，历史评估结果不会被删除，因此如果您改变主意并稍后重新启用策略，之前评估的结果仍然可用。

禁用策略的步骤：

1. 前往 Docker Scout 仪表板中的[策略页面](https://scout.docker.com/reports/policy)。
2. 选择您要禁用的策略。
3. 选择 **Disable** 按钮。

## 删除策略

当您删除策略时，该策略的评估结果也会被删除，不再出现在 Docker Scout 仪表板或 CLI 中。

删除策略的步骤：

1. 前往 Docker Scout 仪表板中的[策略页面](https://scout.docker.com/reports/policy)。
2. 选择您要删除的策略。
3. 选择 **Delete** 按钮。

## 恢复已删除的策略

如果您已删除策略，可以按照[添加策略](#add-a-policy)中的步骤重新创建它。在策略配置屏幕上，选择您希望重新创建的已删除策略上的 **Configure**。
