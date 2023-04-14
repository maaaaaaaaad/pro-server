import { HttpException } from '@nestjs/common'

export class BaseOutputDto {
  access: boolean
  message: string
}

export type CoreOutputDto = BaseOutputDto | HttpException
