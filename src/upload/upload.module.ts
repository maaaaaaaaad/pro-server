import { Module } from '@nestjs/common'
import { UploadController } from './upload.controller'
import { AuthModule } from '../auth/auth.module'
import { ItemModule } from '../item/item.module'

@Module({
  imports: [AuthModule, ItemModule],
  controllers: [UploadController],
})
export class UploadModule {}
